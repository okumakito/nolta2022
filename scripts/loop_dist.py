def loop_dist():
  param_dict['n'] = int(1e5)
  while True:
    x_arr = sde()
    if check_condition(x_arr, None, mode='x_u'):
      break
  sr = pd.Series(x_arr)
  sr = sr.round(5)
  sr.to_csv('tmp.csv', header=None, index=None)
  return sr
    
if __name__ == '__main__':
  res_dist_sr = loop_dist()
