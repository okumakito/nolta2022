def plot_bifurc():

  h = 0.1
  n_div = 1000
    
  # upper branch
  x = 0.8
  x2 = 0.5
  x_high_list = []
  c_high_list = []
  for c in np.linspace(0, 0.35, n_div):
    x_next = fsolve(f_args, x, args=(h,c))[0]
    x2_next = fsolve(df_args, x2, args=(h,c))[0]
    if f_args(x2_next, *(h,c)) < 0:
      break
    x = x_next
    x2 = x2_next
    x_high_list.append(x)
    c_high_list.append(c)

  # lower branch
  x = 0.05
  x2 = 0.2
  x_low_list = []
  c_low_list = []
  for c in np.linspace(0.35, 0, n_div):
    x_next = fsolve(f_args, x, args=(h,c))[0]
    x2_next = fsolve(df_args, x2, args=(h,c))[0]
    if f_args(x2_next, *(h,c)) > 0:
      break
    x = x_next
    x2 = x2_next
    x_low_list.append(x)
    c_low_list.append(c)

  # unstable point
  x += 0.1
  x_mid_list = []
  c_mid_arr = np.linspace(c_low_list[-1], c_high_list[-1], n_div)
  for c in c_mid_arr:
    x = fsolve(f_args, x, args=(h,c))[0]
    x_mid_list.append(x)
  
  fig, ax = plt.subplots(figsize=(6,4))
  plt.plot(c_high_list, x_high_list, 'k')
  plt.plot(c_low_list, x_low_list, 'k')
  plt.plot(c_mid_arr, x_mid_list, 'k--')
  ax.axhline(y=0, c='k', ls='--')
  ax.set_xlim((0,0.35))
  ax.set_ylim((-0.05,1.05))
  ax.set_xlabel('c (consumption rate)')
  ax.set_ylabel('x (population size)')
  ax.tick_params(length=5)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')
    
if __name__ == '__main__':
  plot_bifurc()
