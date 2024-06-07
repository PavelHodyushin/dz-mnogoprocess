from multiprocessing import Process, Manager


class WarehouseManager:
    def __init__(self):    # Атрибут data - словарь, где ключ - название продукта, а значение - его кол-во.
        self.data = Manager().dict()     # словарь изначально пустой


    def process_request(self, request):     # реализует запрос (действие с товаром), принимая request - кортеж.
        name, action, quantity = request
        if action == 'receipt':   # receipt - получение
            if name in self.data:
                self.data[name] = self.data[name] + quantity
            else:
                self.data[name] = quantity
        if action == 'shipment':    # shipment - отгрузка
            if name in self.data and self.data[name] > 0:
                self.data[name] -= quantity


    def run(self, requests):
        processes = []
        for request in requests:
            p = Process(target=self.process_request, args=(request,))
            processes.append(p)
            p.start()
            p.join()


if __name__ == '__main__':
    warehouse_manager = WarehouseManager()     # Создаем менеджера склада
    requests = [                         # Множество запросов на изменение данных о складских запасах
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]
    warehouse_manager.run(requests)     # Запускаем обработку запросов
    print(warehouse_manager.data)      # Выводим обновленные данные о складских запасах
