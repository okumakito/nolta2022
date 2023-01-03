def plot_dist(res_dist_sr):
  h, c, sigma, x_u, x_s = [param_dict[key] for key in
                           ['h', 'c','sigma','x_u', 'x_s']]
  n_bin = 100
  mesh_arr = np.linspace(x_u, 0.65, n_bin)
  bin_size = mesh_arr[1] - mesh_arr[0]

  U_arr = U_args(mesh_arr, *(h,c))
  U_arr -= U_arr.min()
  p_arr = np.exp(-2*U_arr / sigma**2)
  p_arr /= p_arr.sum()

  fig, ax = plt.subplots(figsize=(6,4))
  sns.distplot(res_dist_sr, bins=mesh_arr, ax=ax, kde=False, norm_hist=True,
               label='numerical',
               hist_kws=dict(color=plt.cm.tab10(0), alpha=0.5))
  ax.plot(mesh_arr, p_arr / bin_size, color='k', label='theory')
  ax.legend(loc='upper right', frameon=False)
  ax.set_xlabel('x (population size)')
  ax.set_ylabel('probability density')
  ax.set_xlim((0.4, 0.65))
  ax.set_ylim((0, 20))
  ax.axvline(x_s, ls='--', c='k', lw=2)
  kws = dict(marker='o', lw=2, s=100, zorder=100, clip_on=False)
  ax.scatter([x_s], [0], color='k', edgecolors='k', **kws)
  ax.scatter([x_u], [0], color='w', edgecolors='k', **kws)
  ax.tick_params(length=5)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')
    
if __name__ == '__main__':
  plot_dist(res_dist_sr)
