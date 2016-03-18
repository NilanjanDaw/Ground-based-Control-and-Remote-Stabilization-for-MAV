import matplotlib.pyplot as plt
import time

data = []
ax = []
bx = []
cx = []
dx = []


def plot_roll():
    global ax
    print ax
    plt.figure()
    plt.plot(ax, 'blue', label='x')
    plt.xlabel('Time in mS')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.title('Roll Values')
    plt.grid()
    plt.savefig('graph1.png', dpi=600)
    plt.show()


def plot_pitch():
    global bx
    print bx
    plt.figure()
    plt.plot(bx, 'blue', label='x')
    plt.xlabel('Time in mS')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.title('Pitch Values')
    plt.grid()
    plt.savefig('graph2.png', dpi=600)
    plt.show()


def plot_yaw():
    global cx
    print cx
    plt.figure()
    plt.plot(cx, 'blue', label='x')
    plt.xlabel('Time in mS')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.title('Yaw Values')
    plt.grid()
    plt.savefig('graph3.png', dpi=600)
    plt.show()


def plot_thrust():
    global dx
    print dx
    plt.figure()
    plt.plot(dx, 'blue', label='x')
    plt.xlabel('Time in mS')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.title('Thrust Values')
    plt.grid()
    plt.savefig('graph4.png', dpi=600)
    plt.show()


def read():
    global ax
    f = open('data_log_roll.txt', 'r')
    read_data = f.read()
    data = read_data.split(",")
    # print(data)
    i = 0
    for d in data:
        print float(d)
        ax.append(float(d))
        if i == len(data) - 2:
            break
        i += 1
    plot_roll()
    f = open('data_log_pitch.txt', 'r')
    read_data = f.read()
    data = read_data.split(",")
    # print(data)
    i = 0
    for d in data:
        print float(d)
        bx.append(float(d))
        if i == len(data) - 2:
            break
        i += 1
    plot_pitch()
    f = open('data_log_yaw.txt', 'r')
    read_data = f.read()
    data = read_data.split(",")
    # print(data)
    i = 0
    for d in data:
        print float(d)
        cx.append(float(d))
        if i == len(data) - 2:
            break
        i += 1
    plot_yaw()
    f = open('data_log_thrust.txt', 'r')
    read_data = f.read()
    data = read_data.split(",")
    # print(data)
    i = 0
    for d in data:
        print float(d)
        dx.append(float(d))
        if i == len(data) - 2:
            break
        i += 1
    plot_thrust()


read()
