def plot_mae2(res_mae_f, res_mae_u, mode='skew'):
  T_true = 1.31e4
  df1 = res_mae_f.copy()
  df2 = res_mae_u.copy()
  df1['n'] = df1.n.apply(lambda x:f'$N=10^{int(np.log10(x))}$')
  df2['n'] = df2.n.apply(lambda x:f'$N=10^{int(np.log10(x))}$')
  df1['error'] = (df1.logT_pred - np.log10(T_true)).abs()
  df2['error'] = (df2.logT_pred - np.log10(T_true)).abs()
  title1 = 'Least Squares Method'
  title2 = 'Maximum Likelihood Estimation'

  print(df1.groupby('n').mean().error.round(3))
  print(df2.groupby('n').mean().error.round(3))

  if mode == 'skew':
    x_var = 'skew_th'
    x_label = 'threshold of skewness $\\theta$'
    y_max = 2.3
  elif mode == 'skip':
    x_var = 'n_skip'
    x_label = 'resampling interval $k$'
    y_max = 3.0
  else:
    return

  def func_sub(df, ax, title, label):
    sns.pointplot(data=df, x=x_var, y='error', hue='n', ax=ax)
    ax.legend(frameon=False, loc=2)
    ax.tick_params(length=5)
    ax.set_ylim((0, y_max))
    ax.set_xlabel(x_label)
    ax.set_ylabel('$|\log_{10}\hat T-\log_{10}T|$ (absolute error)')
    ax.set_title(title)
    ax.text(-0.18, 0.98, label, ha='right', va='bottom',
            transform=ax.transAxes, fontsize=24)
  
  fig, (ax1,ax2) = plt.subplots(figsize=(6,8), nrows=2)
  func_sub(df1, ax1, title1, 'A')
  func_sub(df2, ax2, title2, 'B')
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')

if __name__ == '__main__':
  #plot_mae2(res_mae_f_skew, res_mae_u_skew, mode='skew')
  plot_mae2(res_mae_f_skip, res_mae_u_skip, mode='skip')
