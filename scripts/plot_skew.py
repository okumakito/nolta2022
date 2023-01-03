def plot_skew(res_skew_df):
  n_repeat = 1000
  n_bin = 100
  mesh_arr = np.linspace(-1.2,1, n_bin)

  df = res_skew_df

  for skew_th in [-0.5, -0.4]:
    print(skew_th, df[df.skew_val<skew_th].groupby('n').count()/n_repeat)

  fig, ax = plt.subplots(figsize=(6,4))
  for n, df_sub in df.groupby('n'):
    dist = stats.rv_discrete(values=(df_sub.skew_val,
                                     np.ones(n_repeat)/n_repeat))
    ax.plot(mesh_arr, dist.cdf(mesh_arr), label=f'$N=10^{int(np.log10(n))}$')
  ax.legend(frameon=True, loc=2, framealpha=1)
  ax.tick_params(length=5)
  ax.set_xlabel('skewness')
  ax.set_ylabel('cumulative probability')
  ax.grid()
  ax.set_xlim((mesh_arr.min(), mesh_arr.max()))
  ax.set_yticks(np.linspace(0,1,6))
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')

if __name__ == '__main__':
  plot_skew(res_skew_df)
