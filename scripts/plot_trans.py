def plot_trans():
  mu_crit = 2 * 3**0.5 / 9
  mu_max = 0.8
  n_point = 200
  x_min, x_max = -1.7, 1.7
  mu_high_arr = np.linspace(-mu_max, mu_crit, n_point)
  mu_mid_arr  = np.linspace(-mu_crit, mu_crit, n_point)
  mu_low_arr  = np.linspace(-mu_crit, mu_max, n_point)

  def f2_args(x, *mu):
    return -x**3 + x - mu
  def U2(x, mu):
    return x**4/4 - x**2/2 + mu*x

  x_high_list = []
  x_mid_list  = []
  x_low_list  = []
  for mu in mu_high_arr:
    x_high_list.append(fsolve(f2_args, 1, args=(mu))[0])
  for mu in mu_mid_arr:
    x_mid_list.append(fsolve(f2_args, 0, args=(mu))[0])
  for mu in mu_low_arr:
    x_low_list.append(fsolve(f2_args, -1, args=(mu))[0])

  i1, i2, i3 = 130, 185, 120
  mu1, x1 = mu_high_arr[i1], x_high_list[i1]
  mu2, x2 = mu_high_arr[i2], x_high_list[i2]
  mu3, x3 = mu_low_arr[i3],  x_low_list[i3]
  
  fig, (ax,ax2) = plt.subplots(figsize=(8,4), ncols=2)
  ax.plot(mu_high_arr, x_high_list, 'k-')
  ax.plot(mu_mid_arr,  x_mid_list,  'k--')
  ax.plot(mu_low_arr,  x_low_list,  'k-')
  ax.set_xlim((-mu_max, mu_max))
  ax.set_ylim((x_min,x_max))
  ax.set_xticks([])
  ax.set_yticks([])
  ax.set_xlabel('bifurcation parameter')
  ax.set_ylabel('state variable')

  # points
  kws = dict(marker='o', lw=2, s=100, zorder=10, edgecolors='k', color='k')
  ax.scatter(mu1, x1, **kws)
  ax.scatter(mu2, x2, **kws)
  ax.scatter(mu3, x3, **kws)
  d = 0.2
  kws2= dict(ha='center')
  ax.text(mu1, x1+d, 'S1', **kws2)
  ax.text(mu2, x2+d, 'S2', **kws2)
  ax.text(mu3, x3+d, 'S3', **kws2)

  x_arr = np.linspace(x_min, x_max, n_point)
  sep = 1
  ax2.plot(x_arr, U2(x_arr, mu1), 'k-')
  ax2.plot(x_arr, U2(x_arr, mu2)-sep, 'k-')
  ax2.plot(x_arr, U2(x_arr, mu3)-2*sep, 'k-')
  ax2.scatter(x1, U2(x1, mu1), **kws)
  ax2.scatter(x2, U2(x2, mu2)-sep, **kws)
  ax2.scatter(x3, U2(x3, mu3)-2*sep, **kws)
  ax2.text(x1, U2(x1, mu1)+d, 'S1', **kws2)
  ax2.text(x2, U2(x2, mu2)-sep+d, 'S2', **kws2)
  ax2.text(x3, U2(x3, mu3)-2*sep+d, 'S3', **kws2)
  ax2.set_xlim((x_min, x_max))
  ax2.set_xticks([])
  ax2.set_yticks([])
  ax2.set_xlabel('state variable')
  ax2.set_ylabel('potential')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')

if __name__ == '__main__':
  plot_trans()
