def loop_mae():
  n_repeat = 1000
  n_list = [10**3, 10**4, 10**5]
  #skip_list = [1]
  #skew_list = [-0.5, -0.4, -0.3, -0.2, -0.1, 0]
  skip_list = [1, 10, 100, 1000, 10000] # for mle
  #skip_list = [1, 2, 3, 5, 10] # for polyfit
  skew_list = [-0.5]
  param_arr = np.array(np.meshgrid(n_list, skew_list, skip_list))\
                .T.reshape(-1,3)
  use_sde = True # True: sde, False, iid
  use_mle = True # True: mle, False, polyfit

  result_list = []
  for n, skew_th, n_skip in param_arr:
    n, n_skip = int(n), int(n_skip)
    param_dict['n'] = n
    if n_skip >= n:
      continue
    for _ in range(n_repeat):

      while True:
        # generate samples
        if use_sde: # sde
          x_arr  = sde()
          x_arr, dx_arr = calc_dx(x_arr, n_skip)
        else: # iid
          x_arr, dx_arr = gen_iid()

        # calc f_pred
        f_pred = np.poly1d(np.polyfit(x_arr, dx_arr, deg=2))
        sigma_pred = calc_sigma_pred(x_arr, dx_arr, f_pred)
        if use_mle: # True: mle, False: polyfit
          g_pred = mle(x_arr)
          f_pred = -np.polyder(g_pred) * sigma_pred**2 / 2

        # check
        if check_condition(x_arr, f_pred, mode='x_u', skew_th=skew_th):
          break

      # estimate other variables
      x_u_pred, x_s_pred = np.sort(f_pred.r)
      U_pred = -np.polyint(f_pred)
      df_pred = np.polyder(f_pred)
      logT_pred = np.log(2 * np.pi / df_pred(x_u_pred)) + \
                  2*(U_pred(x_u_pred) - U_pred(x_s_pred))/sigma_pred**2
      logT_pred *= np.log10(np.e)

      # output
      result_list.append(dict(n=n,
                              skew_th=skew_th,
                              n_skip=n_skip,
                              x_s_pred=x_s_pred,
                              x_u_pred=x_u_pred,
                              sigma_pred=sigma_pred,
                              logT_pred=logT_pred,
                              df_xs_pred=df_pred(x_s_pred),
                              dU_pred=U_pred(x_u_pred)-U_pred(x_s_pred)))

  df = pd.DataFrame(result_list).round(6)
  df.to_csv('tmp.csv', index=None)
  return df

if __name__ == '__main__':
  t0 = time.time()
  result_df = loop_mae()
  print(f'time = {time.time() - t0:g} s')
