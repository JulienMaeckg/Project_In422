import matplotlib.pyplot as plt

C = [ 2, 3, 2, 2, 2, 2, 3]
Ti = [10, 10, 20, 20, 40, 40, 80]

def GCD(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def LCM(a, b):
    return abs(a * b) // GCD(a, b)

def hyperperiod(L):
    resultat = L[0]
    for i in range(1, len(L)):
        resultat = LCM(resultat, L[i])
    return resultat

lim = hyperperiod(Ti)
maxi = lim + 1

nbTasks = len(C)

tot = sum(C[i] / Ti[i] for i in range(nbTasks))

if tot <= 1:
    print(f"{tot} ==> Schedulable")
else:
    print(f"{tot} ==> Not schedulable")

if tot <= 1:
    schedule = []
    time = []
    
    t = 0
    current_task = None
    time_left = 0
    executions = [0] * nbTasks
    
    while t < lim:
        time.append(t)
        if current_task is not None:
            schedule.append(current_task)
            time_left -= 1
            if time_left == 0:
                executions[current_task] += 1
                current_task = None
            t += 1
            continue
        margins = []
        for task in range(nbTasks):
            period = Ti[task]
            release_time = (t // period) * period
            executions_in_period = schedule[release_time:t].count(task)
            if executions_in_period == 0 and t + C[task] <= release_time + period:
                margin = period - (t % period)
            else:
                margin = maxi
            margins.append(margin)
        mini = min(margins)
        ind = margins.index(mini)
        if mini < maxi:
            current_task = ind
            time_left = C[ind]
            schedule.append(ind)
            time_left -= 1
            if time_left == 0:
                executions[ind] += 1
                current_task = None
        else:
            schedule.append(None)
        t += 1
    
    height = [1] * len(schedule)
    colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple',
     'pink', 'brown', 'grey', 'black', 'lime', 'olive', 'teal', 'navy',
     'magenta', 'gold', 'crimson', 'indigo', 'coral', 'darkgreen', 'darkblue',
     'darkred', 'chocolate', 'firebrick', 'forestgreen', 'maroon', 'mediumblue',
     'darkorange', 'slateblue', 'tomato', 'darkviolet', 'lightgray']
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    for i in range(lim):
        if schedule[i] is not None:
            ax1.bar(time[i] + 0.5, height[i], width=1, color=colors[schedule[i]], edgecolor='black')
    
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(len(C))]
    labels = [f'Task {i + 1}' for i in range(len(C))]
    ax1.legend(handles, labels, title="Tasks", bbox_to_anchor=(1, 0.6), loc='upper left')
    ax1.set_xlabel('Time')
    ax1.set_yticks([])
    ax1.set_xlim(0, lim)
    ax1.set_ylim(0, 1)
    ax1.set_xticks(list(range(0, lim + 1, 10)))
    ax1.set_xticks(list(range(0, lim, 1)), minor=True)
    ax1.tick_params(axis='x', which='both', bottom=True, top=False)
    ax1.tick_params(axis='x', which='minor', length=4, color='gray')
    
    height_bar = 0.8
    task_segments = {}
    for t, task_id in enumerate(schedule):
        if task_id is not None:
            if task_id not in task_segments:
                task_segments[task_id] = []
            if len(task_segments[task_id]) == 0 or task_segments[task_id][-1][1] != t:
                task_segments[task_id].append([t, t + 1])  # start, end
            else:
                task_segments[task_id][-1][1] += 1
    
    yticks = []
    yticklabels = []
    
    for idx, (task_id, segments) in enumerate(task_segments.items()):
        for seg in segments:
            ax2.barh(y=idx, width=seg[1] - seg[0], left=seg[0], height=height_bar,
                     color=colors[task_id], edgecolor='black')
        yticks.append(idx)
        yticklabels.append(f'Task {task_id + 1}')
    
    ax2.set_yticks(yticks)
    ax2.set_yticklabels(yticklabels)
    ax2.set_xlabel('Time')
    ax2.set_xlim(0, lim)
    ax2.grid(True, axis='x', linestyle='--', alpha=0.5)
    fig.suptitle("Task Scheduling")
    plt.tight_layout()
    plt.show()

    WT = {}
    RT = {}
    for task in range(nbTasks):
        WT[task + 1] = []
        RT[task + 1] = []
    WT["tot"] = 0
    RT["tot"] = 0
    
    for task in range(nbTasks):
        for i in range(0, lim, Ti[task]):
            a = schedule[i:i+Ti[task ]].index(task)
            b = len(schedule[i:i+Ti[task]]) - schedule[i:i+Ti[task]][::-1].index(task)
            WT[task + 1].append(a)
            RT[task + 1].append(b)
            WT["tot"] += a
            RT["tot"] += a
            
    print(f"Waiting time: {WT['tot']}")
    print(f"Responding time: {RT['tot']}")