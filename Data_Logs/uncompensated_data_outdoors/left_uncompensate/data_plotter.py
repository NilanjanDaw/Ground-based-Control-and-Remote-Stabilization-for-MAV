import matplotlib.pyplot as plt
import time

data = []
ax = []
bx = []
cx = []
dx = []

def plot():
    global ax, bx, cx, dx
    plt.figure()
    plt.subplot(311)
    plt.plot(ax, 'blue', label='Roll')
    plt.ylabel(r'$\phi$')
    plt.legend()
    plt.title('Telemetry Values')
    plt.grid()
    plt.subplot(312)
    plt.plot(bx, 'blue', label='Pitch')
    plt.xlabel('Time in ms')
    plt.ylabel(r'$\theta$')
    plt.legend()
    plt.grid()
    plt.subplot(313)
    plt.plot(cx, 'blue', label='Yaw')
    plt.xlabel('Time in ms')
    plt.ylabel(r'$\psi$')
    plt.legend()
    plt.grid()
    plt.savefig('graph5.eps', dpi=1200)
    return 0

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
    plt.savefig('graph1.eps', dpi=1200)
    #plt.show()


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
    plt.savefig('graph2.eps', dpi=1200)
    #plt.show()


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
    plt.savefig('graph3.eps', dpi=1200)
   # plt.show()


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
    plt.savefig('graph4.eps', dpi=1200)
    #plt.show()


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
    plot()

read()
