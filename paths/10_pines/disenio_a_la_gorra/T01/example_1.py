from .time import Time

class Example:

    def test(self):
        webminar_starting_time = Time()
        now = Time()
        # 1er problema, el modelo no me enseña que compone una hora
        # Pero además, el modelo no representa acabadamente aquello para lo que lo creo
        webminar_starting_time.hour = 19
        webminar_starting_time.minute = 0
        webminar_starting_time.second = 0 # Recién acá es una hora

        now.hour = 20
        assert (now.hour - webminar_starting_time.hour) == 1, "El resultado debe ser 1"

if __name__ == "__main__":
    test = Example()
    test.test()
