import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time, sys
from scipy import stats
from scipy.optimize import fsolve
from numba import jit

sns.set_context('talk', font_scale=0.8)

import warnings
#warnings.filterwarnings('ignore', 'The iteration is not making good progress')
warnings.filterwarnings('ignore')

# for embedding fonts into pdf figures
import matplotlib
#matplotlib.rcParams['pdf.fonttype'] = 42
#matplotlib.rcParams['ps.fonttype'] = 42

# global variables
param_dict = dict(h        = 0.1,
                  c        = 0.257,
                  dt       = 0.1,
                  sigma    = 0.01,
                  n        = 10000,
                  x_s      = 0.8,
                  x_u      = 0.4,
                  x_c      = 0.3)

def f_args(x, *args):
  h, c = args  
  return x * (1 - x) - c * x**2 / (x**2 + h**2)

def df_args(x, *args):
  h, c = args
  return 1 - 2 * x - 2 * c * x * h**2 / (x**2 + h**2)**2

def U_args(x, *args):
  h, c = args
  return -x**2 / 2 + x**3 / 3 + c*x - c*h*np.arctan(x/h)

def update_equiv(x_s_rough=0.8, x_u_rough=0.4):
  h, c = [param_dict[key] for key in ['h', 'c']]
  param_dict['x_s'] = fsolve(f_args, x_s_rough, args=(h,c))[0]
  param_dict['x_u'] = fsolve(f_args, x_u_rough, args=(h,c))[0]

@jit
def sde(longrun=False):
  # NOTE: complehensions cannot be used with numba
  h        = param_dict['h']
  c        = param_dict['c']
  dt       = param_dict['dt']
  sigma    = param_dict['sigma']
  n        = param_dict['n']
  x        = param_dict['x_s']
  x_c      = param_dict['x_c']
  sqdt_sig = np.sqrt(dt) * sigma
  
  if not longrun:
    x_arr    = np.empty(n)
    for i in range(n):
      x += dt * (x*(1-x) - c * x**2 / (x**2 + h**2)) + \
           sqdt_sig * np.random.randn()
      if x < 0:
        x = 0
      x_arr[i] = x
    return x_arr
  else:
    t = n * dt
    for i in range(n):
      x += dt * (x*(1-x) - c * x**2 / (x**2 + h**2)) + \
           sqdt_sig * np.random.randn()
      if x < x_c:
        t = i * dt
        break
    return t

@jit
def sde_ou():
  dt       = param_dict['dt']
  sigma    = param_dict['sigma']
  n        = param_dict['n']
  x        = 0
  sqdt_sig = np.sqrt(dt) * sigma
  
  x_arr    = np.empty(n)
  for i in range(n):
    x += -10.0 * dt * x + sqdt_sig * np.random.randn()
    x_arr[i] = x
  return x_arr

# NOTE: this calculation is quite slow inside jit
def calc_dx(x_arr, n_skip=1):
  dt = param_dict['dt']
  dx_arr = np.diff(x_arr) / dt
  return x_arr[:-1][::n_skip], dx_arr[::n_skip]

def mle(x_arr, mesh_arr=None, deg=3):
  m_list = [(x_arr**k).mean() for k in range(2*deg-1)]
  A = np.zeros((deg, deg))
  for i in range(deg):
    for j in range(deg):
      A[i,j] = (i+1)*(j+1)*m_list[i+j]
  b = np.zeros(deg)
  for i in range(1,deg):
    b[i] = (i+1)*i*m_list[i-1]
  b = b.reshape(-1,1)
  coef_arr = np.linalg.inv(A).dot(b).reshape(-1)
  g_pred = np.poly1d(np.r_[coef_arr[::-1], 0])
  if np.any(mesh_arr):
    g_pred = np.poly1d(np.r_[g_pred.c[:-1], -g_pred(mesh_arr).min()])
  return g_pred

def gen_mesh(n_mesh, x_max=0.65):
  x_u      = param_dict['x_u']
  n_bin    = np.ceil(np.sqrt(n_mesh)).astype(int)
  mesh_arr = np.linspace(x_u, x_max, n_bin)
  bin_size = mesh_arr[1] - mesh_arr[0]
  return mesh_arr, bin_size

def p_theory(mesh_arr):
  h, c, sigma = [param_dict[key] for key in ['h','c','sigma']]
  U_arr  = U_args(mesh_arr, *(h,c))
  U_arr -= U_arr.min()
  p_arr  = np.exp(-2*U_arr / sigma**2)
  p_arr /= p_arr.sum()
  return p_arr

def gen_iid():
  h, c, sigma, dt, x_s, x_u, n = [param_dict[key] for key in
                                  ['h','c','sigma','dt','x_s','x_u','n']]
  # NOTE: more than 20% points are selected in most cases
  x_arr  = (0.65 - x_u) * np.random.rand(5*n) + x_u
  U_arr  = U_args(x_arr, *(h,c))
  U_arr -= U_arr.min()
  p_arr  = np.exp(-2*U_arr / sigma**2)
  p_arr /= p_arr.max()
  x_arr  = x_arr[p_arr > np.random.rand(len(p_arr))]
  x_arr  = np.random.choice(x_arr, n, replace=False)
  dx_arr = f_args(x_arr, *(h,c)) + \
    sigma * np.random.randn(len(x_arr)) / np.sqrt(dt)
  return x_arr, dx_arr

def check_condition(x_arr, f_pred, mode='x_u', skew_th=None):
  x_u, x_c = [param_dict[key] for key in ['x_u','x_c']]
  if mode=='x_u':
    x_th = x_u
  elif mode == 'x_c':
    x_th = x_c
  else:
    mode == np.inf

  # min value
  if x_arr.min() < x_th:
    return False

  # skewness
  if skew_th:
    if stats.skew(x_arr) > skew_th:
      return False

  if f_pred:
    # convex direction
    if f_pred.c[0] > 0:
      return False

    # real roots
    x_u_pred, x_s_pred = np.sort(f_pred.r)
    if x_u_pred.imag != 0:
      return False

    # x_u_pred
    if x_u_pred < x_c:
      return False

    # x_s_pred
    if (x_s_pred > x_arr.max()) or (x_s_pred < x_arr.min()):
      return False

  # all passed
  return True

def calc_sigma_pred(x_arr, dx_arr, f_pred):
  dt = param_dict['dt']
  return np.std(dx_arr - f_pred(x_arr), ddof=1) * np.sqrt(dt)

def calc_sigma_pred2_old(x_arr, dx_arr, g_pred):
  dt = param_dict['dt']
  tau_rough = 0.01**2
  dx2_arr = dx_arr * np.sqrt(dt)
  y_arr = np.polyder(g_pred)(x_arr) * np.sqrt(dt) / 2
  def L(tau):
    return np.var(dx2_arr + tau*y_arr, ddof=1)-tau
  tau = fsolve(L, tau_rough)[0]
  return tau**0.5

def calc_sigma_pred2(x_arr, dx_arr, g_pred):
  dt = param_dict['dt']
  dx2_arr = dx_arr * np.sqrt(dt)
  y_arr = np.polyder(g_pred)(x_arr) * np.sqrt(dt) / 2
  tau = np.poly1d([y_arr.var(ddof=1),
                   2 * np.cov(dx2_arr, y_arr, ddof=1)[0,1] - 1,
                   dx2_arr.var(ddof=1)]).r.min()
  return tau**0.5

if __name__ == '__main__':
  update_equiv()
  plt.plot()
  plt.close()
