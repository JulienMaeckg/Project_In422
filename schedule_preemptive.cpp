#include <iostream>

int GCD(int a, int b) {
    int a_ = a;
    int b_ = b;
    int c = 0;
    while (b_ != 0) {
        c = b_;
        b_ = a_ % b_;
        a_ = c;
    }
    return a_;
}

int abs(int a) {
    if (a < 0) {
        return -a;
    }
    return a;
}

int LCM(int a, int b) {
    return abs(a * b) / GCD(a, b);
}

int hyperperiod(int* List, int len) {
    int res = List[0];
    for (int i = 1; i < len; i++) {
        res = LCM(res, List[i]);
    }
    return res;
}

int min(int* List, int len) {
    int mini = List[0];
    for (int i = 1; i < len; i++) {
        if (List[i] < mini) {
            mini = List[i];
        }
    }
    return mini;
}

int max(int* List, int len) {
    int maxi = List[0];
    for (int i = 1; i < len; i++) {
        if (List[i] > maxi) {
            maxi = List[i];
        }
    }
    return maxi;
}

void sublist(int* ListA, int* ListB, int start, int size) {
    for (int i = 0; i < size; i++) {
        ListB[i] = ListA[i + start];
    }
}

int count(int* List, int len, int x) {
    int nb = 0;
    for (int i = 0; i < len; i++) {
        if (List[i] == x) {
            nb += 1;
        }
    }
    return nb;
}

int index(int* List, int len, int x) {
    int ind = 0;
    for (int i = len - 1; i >= 0; i--) {
        if (List[i] == x) {
            ind = i;
        }
    }
    return ind;
}

void ones(int* List, int len) {
    for (int i = 0; i < len; i++) {
       List[i] = -1;
    }
}

void taskNumber(int* List, int len) {
    for (int i = 0; i < len; i++) {
        if (List[i] != -1) {
            List[i]++;
        }
    }
}

void printList(int* List, int len) {
    for (int i = 0; i < len; i++) {
       std::cout << List[i] << " ";
    }
    std::cout << std::endl;
}

void scheduler(int* schedule, int* C, int* Ti,  const int len) {
    const int lim = hyperperiod(Ti, len);
    int maxi = lim + 1;
    int margins[len];
    int t = 0;
    int limit;
    int duration;
    int actual;
    int inf;
    int done;
    int margin;
    int mini;
    int ind;
    ones(schedule, lim);
    while (t < lim) {
        for (int task = 0; task < len; task++) {
            limit = Ti[task];
            duration = C[task];
            actual = t % limit;
            inf = (t / limit) * limit;
            int* ListB = new int [limit];
            ones(ListB, limit);
            sublist(schedule, ListB, inf, limit);
            done = count(ListB, limit, task);
            delete ListB;

            if (done < duration) {
                margin = limit - actual;
            } else {
                margin = maxi;
            }
            margins[task] = margin;
        }
        mini = min(margins, len);
        ind = index(margins, len, mini);
        if (mini < maxi) {
            schedule[t] = ind;
        } else {
            schedule[t] = -1;
        }
        t += 1;
    }
    taskNumber(schedule, lim);
    std::cout << "Hyperperiod: " << lim << std::endl;
    printList(schedule, lim);
}

int main(void) {
    int C[] = {2, 3, 2, 2, 2, 2, 3};
    int Ti[] = {10, 10, 20, 20, 40, 40, 80};
    const int len = 7;
    const int lim = max(Ti, len);
    int schedule[lim];
    scheduler(schedule, C, Ti, len);
    return 0;
}