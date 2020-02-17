#!/usr/local/bin/python3
#
# Paul Evans (10evans@cua.edu
# 15 February 2020
#
import math
import matplotlib.pyplot as pp
import statistics

def regression_slope(data_points):
    n = len(data_points)
    x_values, y_values = zip(*data_points)
    x_bar = statistics.mean(x_values)
    y_bar = statistics.mean(y_values)
    xy_sum = 0
    x_squared_sum = 0
    for i in range(n):
        xy_sum += x_values[i] * y_values[i]
        x_squared_sum += x_values[i] ** 2
    return (xy_sum - n * x_bar * y_bar) / (x_squared_sum - n * x_bar **2)

def plot_regression(data_points):
    x_values, y_values = zip(*data_points)
    x_bar = statistics.mean(x_values)
    y_bar = statistics.mean(y_values)
    slope = regression_slope(data_points)
    x_values = [0, max(x_values)]
    y_values = []
    for x in x_values:
        y_values.append(y_bar + slope * (x - x_bar))
    pp.plot(x_values, y_values)
    return slope

def plot_data_bar(data_points):
    x_values, y_values = zip(*data_points)
    pp.bar(x_values, y_values)
    pp.xticks([1, 5, 10, 15, 20])
    pp.xlabel('rank')
    pp.ylabel('word count')

def plot_data_scatter(data_points):
    x_values, y_values = zip(*data_points)
    pp.scatter(x_values, y_values)
    pp.xlabel('$log_{e}$ rank')
    pp.ylabel('$log_{e}$ word count')

def logify(data_points):
    x_tmp, y_tmp = zip(*data_points)
    x_values = list(x_tmp)
    y_values = list(y_tmp)
    x_log = [math.log(x) for x in x_values]
    y_log = [math.log(y) for y in y_values]
    return list(zip(x_log, y_log))

def main():
    # theoretical Zipf distribution for 20 MFWs (bar plot)
    x_tmp = [x for x in range(1, 21)]
    y_tmp = [(1 / x) * 1861 for x in x_tmp]
    plot_data_bar(list(zip(x_tmp, y_tmp)))
    pp.title('theoretical Zipf distribution for 20 MFWs')
    pp.savefig('PNGs/Zipf_0.png')
    pp.show()
    # theoretical Zipf distribution for 20 MFWs (log-log scatter plot)
    plot_data_scatter(logify(list(zip(x_tmp, y_tmp))))
    slope = plot_regression(logify(list(zip(x_tmp, y_tmp))))
    pp.title(f'theoretical Zipf distribution for 20 MFWs\n(log-log, slope = {slope:.4f})')
    pp.savefig('PNGs/Zipf_1.png')
    pp.show()
    #  actual distribution for 20 MFWs from R1 and R2 dicta (bar plot)
    data_points = [(1, 1861), (2, 1666), (3, 1638), (4, 1132), (5, 784), (6, 768), (7, 691), (8, 681), (9, 677), (10, 661), (11, 631), (12, 534), (13, 530), (14, 518), (15, 510), (16, 473), (17, 418), (18, 379), (19, 372), (20, 357)]
    plot_data_bar(data_points)
    pp.title('actual distribution for 20 MFWs from R1 and R2 $\it{dicta}$')
    pp.savefig('PNGs/Zipf_2.png')
    pp.show()
    # actual distribution for 20 MFWs from R1 and R2 dicta (log-log scatter plot)
    plot_data_scatter(logify(data_points))
    slope = plot_regression(logify(data_points))
    pp.title('actual distribution for 20 MFWs from R1 and R2 $\it{dicta}$\n(log-log, slope = ' + f'{slope:.4f})')
    pp.savefig('PNGs/Zipf_3.png')
    pp.show()

if __name__ == "__main__":
    main()

