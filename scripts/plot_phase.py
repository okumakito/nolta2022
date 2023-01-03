def calc_bifurc_point(h=0.1, plot_fig=True):
  n_div = 100
  # high 
  if True:
    x = 0.5
    y = 0.25
    c = 0.0
    for c_next in np.linspace(0,1,n_div):
      x_next = fsolve(df_args, x, args=(h,c_next))[0]
      y_next = f_args(x_next, *(h,c_next))
      #print(c_next, x_next, y_next)
      if y_next < 0:
        c_high = c + (c_next - c) * y / (y + np.abs(y_next))
        break
      x = x_next
      y = y_next
      c = c_next
    #print('high', c_high)

  # low
  if True:
    x = np.sqrt(h)/2
    y = -0.2
    c = 0.3
    for c_next in np.linspace(0.3,0,n_div):
      x_next = fsolve(df_args, x, args=(h,c_next))[0]
      y_next = f_args(x_next, *(h,c_next))
      #print(c_next, x_next, y_next)
      if y_next > 0:
        c_low = c + (c_next - c) * np.abs(y) / (np.abs(y) + y_next)
        break
      x = x_next
      y = y_next
      c = c_next
    #print('low ', c_low)

  if plot_fig:
    h = 0.1
    c = 0.35
    c = c_high
    print(h,c)
    fig, ax = plt.subplots()
    x_arr = np.linspace(0,1,200)
    ax.plot(x_arr, f_args(x_arr, *(h,c)))
    ax.axhline(y=0)
    fig.show()

  return c_high, c_low

def plot_phase():
  c_high_list = []
  c_low_list = []
  h_arr = np.linspace(0.001, 0.196, 100)
  for h in h_arr:
    c_high, c_low = calc_bifurc_point(h, plot_fig=False)
    c_high_list.append(c_high)
    c_low_list.append(c_low)

  fig, ax = plt.subplots(figsize=(6,4))
  ax.plot(c_high_list, h_arr, 'k')
  ax.plot(c_low_list, h_arr, 'k')
  ax.set_xlim((0,0.35))
  ax.set_ylim((0,0.25))
  ax.set_xlabel('c (consumption rate)')
  ax.set_ylabel('h (half-saturation constant)')
  ax.text(0.10, 0.20, 'monostable', ha='center', va='center')
  ax.text(0.18, 0.05, 'bistable', ha='center', va='center')
  ax.text(0.29, 0.23, 'cusp point', ha='center', va='center')
  ax.arrow(0.29, 0.22, 0.005, -0.01, head_width=0.008, fc='k')
  ax.tick_params(length=5)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')
    
if __name__ == '__main__':
  #calc_bifurc_point()
  plot_phase()
