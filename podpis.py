import plotly.express as px

# h_k = x_k - x_(k-1)
def h(x_arr):
    h_arr = [0.0] 
    for i in range(1, len(x_arr)): 
        h_arr.append(x_arr[i] - x_arr[i - 1])
    return h_arr

# lambda_k = h_k/(h_k + h_(k+1))
def lambdas(h_arr):
    lambda_arr = [0.0]
    for i in range(1, (len(h_arr) - 1)): 
        lambda_arr.append(h_arr[i] / (h_arr[i] + h_arr[i + 1])) 
          
    return lambda_arr

# d_k = 6 * f[x_(k-1), x_k, x(k+1)]
def d(x_arr, y_arr):
    d_arr = [0.0]
    for i in range(1, len(x_arr) - 1):
        d_arr.append(6 * ((((y_arr[i + 1] - y_arr[i]) / (x_arr[i + 1] - x_arr[i]))
        - ((y_arr[i] - y_arr[i - 1]) / (x_arr[i] - x_arr[i - 1])))
        / (x_arr[i + 1] - x_arr[i - 1])))
    return d_arr

#recursive computation of consecutive moments
def moments(x_arr, y_arr):
    p = [0.0]
    q = [0.0]
    v = 0.0

    h_array = h(x_arr)
    lambda_array = lambdas(h_array)
    d_array = d(x_arr, y_arr)
    
    # M_n = 0
    m_array = [0]

    for i in range (1, len(lambda_array)):
        v = (lambda_array[i] * p[i - 1] + 2.0)
        p.append((lambda_array[i] - 1.0) / v)
        q.append((d_array[i] - lambda_array[i] * q[i - 1]) / v)

    # M_n-1 = q_n-1
    m_array.insert(0, q[len(q) - 1])

    # M_k = p_k * M[k+1] + q[k]
    for i in range (len(q) - 2, -1, -1):
        m_array.insert(0, p[i] * m_array[0] + q[i])

    return m_array

#s_k
def nifs3(x_arr, y_arr, h_arr, m_arr, k):
    return (lambda x : ((1.0 / h_arr[k]) * (((1.0 / 6.0) * m_arr[k - 1] * (x_arr[k] - x) ** 3) 
    + ((1.0 / 6.0) * m_arr[k] * (x - x_arr[k - 1]) ** 3)
    + (y_arr[k - 1] - ((1.0 / 6.0) * m_arr[k - 1] * h_arr[k] ** 2)) * (x_arr[k] - x) 
    + (y_arr[k] - ((1.0 / 6.0) * m_arr[k] * h_arr[k] ** 2)) * (x - x_arr[k - 1]))))


#s_k(x), s_k(y)
def f_s(x_arr, y_arr):
    s_x = []
    s_y = []
    t = []
    M = 3000
    n = len(x_arr) - 1

    # time array
    for k in range (0, len(x_arr)):
        t.append(k / n)

    m_x = moments(t, x_arr)
    m_y = moments(t, y_arr)

    h_arr = h(t)
    x_array = []
    y_array = []

    for k in range (1, len(x_arr)):
        x_array.append(nifs3(t, x_arr, h_arr, m_x, k))
        y_array.append(nifs3(t, y_arr, h_arr, m_y, k))
    
    index = 1
    for k in range(M + 1):
        u = k / M
        if (index < (len(x_array) + 1) and u > t[index]): index += 1
        s_x.append(x_array[index - 1](u))
        s_y.append(y_array[index - 1](u))

    return s_x, s_y

# auxiliary function for file input
def get_coordinates(points):
    axis = 1
    x_arr = []
    y_arr = []
    for coord in points:
        if axis:
            x_arr.append(float(coord))
            axis = 0
        else:
            y_arr.append(float(coord))
            axis = 1
    return x_arr, y_arr


def print_nifs3():
    with open("input.txt", 'r') as file:
        letters = file.readlines()
    
    letters = [points.split(' ') for points in letters]

    fig = px.line(range_x=[0, 60], range_y=[0, 60])

    for points in letters:
        x_arr, y_arr = get_coordinates(points)
        s_x, s_y = f_s(x_arr, y_arr)
        fig.add_scatter(x=s_x, y=s_y, line_color = 'darkblue', line_width = 5)

    fig.update_layout(height = 900, width = 900, template='plotly_white')
    fig.show()

print_nifs3()