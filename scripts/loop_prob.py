def loop_prob():
  param_dict['n'] = int(1e7)
  n_repeat = 1000
  #n_repeat = 100

  t0 = time.time()
  t_list = []
  for i in range(n_repeat):
    t = sde(longrun=True)
    t_list.append(t)
  print('time = {:g}s'.format(time.time() - t0))

  sr = pd.Series(t_list)
  sr = sr.round(3)
  sr.to_csv('tmp.csv', header=None, index=None)
  return sr

if __name__ == '__main__':
  res_prob_sr = loop_prob()
