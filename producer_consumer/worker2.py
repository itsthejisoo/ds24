from listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self, items, boarding_cus):
        self.__alive = True
        self.items = items
        self.boarding_cus = boarding_cus
        self.worker = threading.Thread(target=self.run)

    def run(self):
        while True:
            time.sleep(0.2)
            if self.__alive:
                if not self.items.isEmpty():
                    item = self.items.dequeue()
                    self.boarding_cus.enqueue(item)
                    print("Arrived:", item[1])
                else:
                    print("No more passenger")
            else:
                break
        
        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()

class Consumer:
    def __init__(self, items, boarding_cus):
        self.__alive = True
        self.worker = threading.Thread(target=self.run)
        self.items = items
        self.boarding_cus = boarding_cus

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:
                if not self.boarding_cus.isEmpty():
                    item = self.boarding_cus.dequeue()
                    print("Boarding:", item[1])
                else:
                    print("All passengers on flight")
            else:
                break

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()

if __name__ == "__main__":
    
    customers = ListQueue()  # 우선순위 큐 생성
    boarding_customer = ListQueue()

    with open("./customer.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            customer = line.split()
            grade = int(customer[0])
            name = customer[1]
            customers.enqueue((grade, name))

    producer = Producer(customers, boarding_customer)
    consumer = Consumer(customers, boarding_customer)
    producer.start()
    consumer.start()
    time.sleep(10)
    producer.finish()
    consumer.finish()
