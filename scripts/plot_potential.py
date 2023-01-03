def plot_potential():
  h = param_dict['h']
  c_list = [0.22, 0.25, 0.28]
  
  fig, ax = plt.subplots(figsize=(6,4))
  x_arr = np.linspace(0,1.0,100)
  for c in c_list:
    plt.plot(x_arr, U_args(x_arr, *(h,c)), label=f'c={c}')
  ax.legend(frameon=False)
  ax.set_xlim((0,1.0))
  ax.set_ylim((-0.01,0.05))
  ax.set_xlabel('x (population size)')
  ax.set_ylabel('U (potential)')
  ax.tick_params(length=5)
  fig.tight_layout()
  fig.show()
  fig.savefig('tmp.png')
  fig.savefig('tmp.pdf')
    
if __name__ == '__main__':
  plot_potential()
