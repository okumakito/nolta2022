def plot_upf():
  h ,c, sigma, x_u, x_s = [param_dict[key] for key in
                           ['h','c','sigma','x_u','x_s']]
  x_min = 0.35
  x_max = 0.65
  
  x_arr = np.linspace(x_min,x_max,100)
  U_arr = U_args(x_arr, *(h,c))
  U_min = U_arr.min()
  U_arr -= U_min
  f_arr = f_args(x_arr, *(h,c))
  p_arr = np.exp(-2*U_arr / sigma**2)
  p_arr[x_arr<x_u] = 0
  
  fig, (ax1,ax2,ax3) = plt.subplots(figsize=(6,4), nrows=3)
  c1, c2, c3 = [plt.cm.tab10(i) for i in range(3)]

  ax1.plot(x_arr, f_arr, c=c1)
  ax2.plot(x_arr, U_arr, c=c2)
  ax3.fill_between(x_arr, p_arr, color=c3)
  ax1.axhline(y=0, c=c1, ls='--')
  
  ax1.set_xticks([])
  ax2.set_xticks([])
  ax1.set_ylim((-0.008,0.005))
  ax2.set_ylim((-0.0001,0.001))
  ax3.set_ylim((0,1.2*p_arr.max()))
  ax3.set_xlabel('x')
  ax1.set_ylabel('f(x)')
  ax2.set_ylabel('U(x)')
  ax3.set_ylabel('p(x)')
  kws = dict(marker='o', lw=2, s=100, zorder=10)
  y_arr = U_args(np.array([x_u,x_s]),*(h,c)) - U_min
  ax1.scatter([x_u], [0], color='w', edgecolors=c1, **kws)
  ax1.scatter([x_s], [0], color=c1, edgecolors=c1, **kws)
  ax2.scatter([x_u], [y_arr[0]], color='w', edgecolors=c2, **kws)
  ax2.scatter([x_s], [y_arr[1]], color=c2, edgecolors=c2, **kws)

  for ax in (ax1,ax2,ax3):
    ax.tick_params(length=5)
    ax.set_xlim((x_min, x_max))
    ax.set_yticks([])
  fig.tight_layout(pad=0.3)
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')

if __name__ == '__main__':
  plot_upf()
