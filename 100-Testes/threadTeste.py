from threading import Thread
import sys
import numpy as np

#documentação https://docs.python.org/release/2.5.2/lib/thread-objects.html


values = {0: [1]*100000000, 1: [3, 2]}
sequential_total = 0
threaded_total = 0
threads = []

class Th(Thread):

    def __init__(self, num):
        sys.stdout.write("Criando Thread numero " + str(num + 1) + "\n")
        sys.stdout.flush()
        Thread.__init__(self)
        self.num = num
        self.subtotal = 0

    def run(self):
        self.subtotal = np.sum(values[self.num])
        sys.stdout.write("Subtotal: " + str(self.get_subtotal()) + "\n")
        sys.stdout.flush()

    def get_subtotal(self):
        return self.subtotal

#### O programa comeca aqui #####

for thread_number in range(2):
       threads.insert(thread_number, Th(thread_number))
       threads[thread_number].start()

threaded_total += threads[0].get_subtotal()
threaded_total += threads[1].get_subtotal()


print("Total: " + str(threaded_total))

'''
threads[thread_number].join(0)
print(thread_number)
'''
