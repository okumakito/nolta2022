def plot_trans_type():
  mu_crit = 2 * 3**0.5 / 9
  mu_max = 0.8
  n_point = 200
  x_min, x_max = -1.5, 1.5
  y_min, y_max = -0.9, 0.9
  z_min, z_max = -1.0, 1.0
  mu_high_arr = np.linspace(-mu_max, mu_crit, n_point)
  mu_mid_arr  = np.linspace(-mu_crit, mu_crit, n_point)
  mu_low_arr  = np.linspace(-mu_crit, mu_max, n_point)
  mu_all_arr  = np.linspace(-mu_max, mu_max, n_point)

  def fx_args(x, *mu):
    return -x**3 + x - mu
  def fz_args(z, *mu):
    return -z**3 - 0.2 * z - mu

  x_high_list = []
  x_mid_list  = []
  x_low_list  = []
  z_list = []
  for mu in mu_high_arr:
    x_high_list.append(fsolve(fx_args, 1, args=(mu))[0])
  for mu in mu_mid_arr:
    x_mid_list.append(fsolve(fx_args, 0, args=(mu))[0])
  for mu in mu_low_arr:
    x_low_list.append(fsolve(fx_args, -1, args=(mu))[0])
  for mu in mu_all_arr:
    z_list.append(fsolve(fz_args, -1, args=(mu))[0])
    
  kws = dict(marker='o', lw=2, s=100, zorder=10, edgecolors='k', color='k')
  kws_text = dict(ha='center', va='center', fontsize=18)
  kws_text2 = dict(ha='right', va='top', fontsize=24)
  kws_ar = dict(width=0.03, head_length=0.12, ec='none',
                fc=plt.cm.tab10(3), zorder=10)
  
  fig, axes = plt.subplots(figsize=(8,6), ncols=2, nrows=2)
  axes = axes.flatten()

  # top left
  ax = axes[0]
  ax.plot(mu_high_arr, x_high_list, 'k-')
  ax.plot(mu_mid_arr,  x_mid_list,  'k--')
  ax.plot(mu_low_arr,  x_low_list,  'k-')
  ax.set_xlim((-mu_max, mu_max))
  ax.set_ylim((x_min,x_max))
  ax.arrow(0.74, 0.7, 0, -0.45, transform=ax.transAxes, **kws_ar)
  ax.text(-0.45, 0.5, 'critical\ntransition', transform=ax.transAxes,
          **kws_text)
  ax.text(0.5, 1.15, 'bifurcation', transform=ax.transAxes, **kws_text)
  ax.text(-0.05, 1, 'A', transform=ax.transAxes, **kws_text2)

  # top right
  ax = axes[1]
  ax.plot(mu_high_arr, x_high_list, 'k-')
  ax.plot(mu_mid_arr,  x_mid_list,  'k--')
  ax.plot(mu_low_arr,  x_low_list,  'k-')
  ax.set_xlim((-mu_max, mu_max))
  ax.set_ylim((x_min,x_max))
  ax.arrow(0.65, 0.78, 0, -0.52, transform=ax.transAxes, **kws_ar)
  ax.text(0.5, 1.15, 'non-bifurcation', transform=ax.transAxes,
          **kws_text)
  ax.text(-0.05, 1, 'B', transform=ax.transAxes, **kws_text2)
  
  # bottom left
  ax = axes[2]
  ax.plot([-mu_max,0], [0,0], 'k-')
  ax.plot([-mu_max,0],  [-mu_max,0],  'k--')
  ax.plot([0,mu_max], [0,mu_max], 'k-')
  ax.plot([0,mu_max], [0,0], 'k--')
  ax.set_xlim((-mu_max, mu_max))
  ax.set_ylim((y_min,y_max))
  ax.arrow(0.4, 0.55, 0.3, 0.25, transform=ax.transAxes, **kws_ar)
  ax.text(-0.45, 0.5, 'non-critical\ntransition', transform=ax.transAxes,
          **kws_text)
  ax.text(-0.05, 1, 'C', transform=ax.transAxes, **kws_text2)

  # bottom right
  ax = axes[3]
  ax.plot(mu_all_arr, z_list, 'k-')
  ax.set_xlim((-mu_max, mu_max))
  ax.set_ylim((z_min,z_max))
  ax.arrow(0.45, 0.85, 0.2, -0.45, transform=ax.transAxes, **kws_ar)
  ax.text(-0.05, 1, 'D', transform=ax.transAxes, **kws_text2)

  for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('bifurcation parameter')
    ax.set_ylabel('state variable')

  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.pdf')

if __name__ == '__main__':
  plot_trans_type()
