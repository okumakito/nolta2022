def plot_prob(res_prob_sr):
  h, c, sigma = [param_dict[key] for key in ['h', 'c','sigma']]
  sr = res_prob_sr

  x_u = fsolve(f_args, 0.4, args=(h,c))[0]
  x_s = fsolve(f_args, 0.8, args=(h,c))[0]
  T = 2 * np.pi / np.sqrt(- df_args(x_s,*(h,c)) * df_args(x_u,*(h,c))) * \
      np.exp(2 * (U_args(x_u,*(h,c)) - U_args(x_s,*(h,c))) / sigma**2)
  print(f'T (theory)    = {T:.2e}')
  print(f'T (numerical) = {sr.mean():.2e}')
  
  n_t = len(sr)
  
  x_arr = np.logspace(np.log10(sr.min()),np.log10(sr.max()))

  fig, ax = plt.subplots(figsize=(6,4))
  ax.semilogx(x_arr, 1 - np.exp(-x_arr/T), 'k', label='theory')
  ax.semilogx(sr.sort_values(), np.arange(1,n_t+1)/n_t, 'k:', lw=3,
              label='numerical')
  ax.legend(loc='upper left', frameon=False)
  ax.set_xlabel('t (time)')
  ax.set_ylabel('cumulative escape probability')
  ax.tick_params(length=5)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')

if __name__ == '__main__':
  plot_prob(res_prob_sr)
