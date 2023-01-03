def loop_skew():
  n_repeat = 1000
  n_list = [10**3, 10**4, 10**5]

  out_list = []
  for n in n_list:
    param_dict['n'] = n
    for _ in range(n_repeat):
      while True:
        x_arr  = sde()
        if check_condition(x_arr, None, mode='x_u'):
          break
      out_list.append((n, stats.skew(x_arr)))
  df = pd.DataFrame(out_list, columns=['n','skew_val'])
  df['skew_val'] = df.skew_val.round(5)
  df.to_csv('tmp.csv', index=None)
  return df

if __name__ == '__main__':
  t0 = time.time()
  res_skew_df = loop_skew()
  print(f'time = {time.time() - t0:g} s')
