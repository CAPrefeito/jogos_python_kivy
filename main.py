from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.animation import Animation
from random import random
import random as random_python

interval_obstacle = 2
interval_gap = 0.5
obstacle_width = 0.07
t_animacao_furacao = 3


class Manager(ScreenManager):
    pass


class Menu(Screen):
    pass


class GameMario(Screen):
    obstacles = []
    score = NumericProperty(0)

    def on_enter(self, *args):
        Clock.schedule_interval(self.update, 1 / 30)
        Clock.schedule_interval(self.put_obstacle, interval_obstacle)

    def on_pre_enter(self, *args):
        self.ids.mario.y = self.height / 2
        self.ids.mario.speed = 0
        self.score = 0

    def update(self, *args):
        self.ids.mario.speed += -self.height*2 * 1 / 30
        self.ids.mario.y += self.ids.mario.speed * 1 / 30
        if self.ids.mario.y > self.height or self.ids.mario.y < 0:
            self.game_over()
        elif self.player_collided():
            self.game_over()

    def on_touch_down(self, touch):
        self.ids.mario.speed = self.height * 0.7

    def put_obstacle(self, *args):
        gap = self.height * interval_gap
        position = (self.height - gap) * random()
        width = self.width * obstacle_width
        obstacle_low = Obstacle(x=self.width, height=position, width=width)
        obstacle_high = Obstacle(x=self.width, y=position + gap, height=self.height - position - gap, width=width)
        self.add_widget(obstacle_low, 3)
        self.add_widget(obstacle_high, 3)
        self.obstacles.append(obstacle_low)
        self.obstacles.append(obstacle_high)

    def game_over(self, *args):
        Clock.unschedule(self.update, 1 / 30)
        Clock.unschedule(self.put_obstacle, interval_obstacle)
        for ob in self.obstacles:
            ob.anim.cancel(ob)
            self.remove_widget(ob)
        self.obstacles = []
        App.get_running_app().root.current = 'gameOver'

    def collided(self, wid1, wid2):
        if wid2.x <= wid1.x + wid1.width and \
                wid2.x + wid2.width >= wid1.x and \
                wid2.y <= wid1.y + wid1.height and \
                wid2.y + wid2.height >= wid1.y:
            return True
        return False

    def player_collided(self, *args):
        collided = False
        for obstacle in self.obstacles:
            if self.collided(self.ids.mario, obstacle):
                collided = True
                break
        return collided


class GameFuracao(Screen):
    obstacles = []
    score = NumericProperty(0)

    # pass
    def on_enter(self, *args):
        Clock.schedule_interval(self.update, 1 / 30)
        # Clock.schedule_interval(self.rain_items, 1)
        Clock.schedule_interval(self.put_obstacle, interval_obstacle)

    def on_pre_enter(self, *args):
        self.score = 0

    def update(self, *args):
        # pass
        self.ids.furacao.speed += -self.height * 3 * 1 / 30
        self.ids.furacao.y += self.ids.furacao.speed * 1 / 30
        if self.ids.furacao.y > self.height:
            self.game_over()
        elif self.ids.furacao.y < 0:
            self.ids.furacao.y = 0
        elif self.rain_items_update():
            self.game_over()

    def game_over(self, *args):
        Clock.unschedule(self.update, 1 / 30)
        Clock.unschedule(self.put_obstacle, interval_obstacle)
        for ob in self.obstacles:
            ob.anim.cancel(ob)
            self.remove_widget(ob)
        self.obstacles = []
        App.get_running_app().root.current = 'gameOver'

    def on_touch_down(self, touch):
        # Clock.schedule_interval(self.update, 1 / 30)
        self.ids.furacao.speed = self.height * 0.7
        # pass

    def on_touch_up(self, touch):
        # Clock.unschedule(self.update, 1 / 30)
        pass

    def on_touch_move(self, touch):
        if touch.x < self.ids.furacao.width / 3:
            self.ids.furacao.center_y = touch.y
        if touch.x > self.ids.furacao.width - self.ids.furacao.width / 3:
            self.ids.furacao.center_y = touch.y
        if touch.y < self.ids.furacao.height / 3:
            self.ids.furacao.center_x = touch.x
        if touch.x > self.ids.furacao.height - self.ids.furacao.height / 3:
            self.ids.furacao.center_x = touch.x

    def put_obstacle(self, *args):
        pos_obs = []
        delta_pos = 20
        opcoes_obs = [2, 3, 4]
        n_ob = random_python.choice(opcoes_obs)
        obs_w = self.height / 6
        obs_h = obs_w / 2

        while len(pos_obs) < n_ob:
            pos = self.width * random()
            pos_wn = pos - obs_w - delta_pos
            pos_wp = pos + obs_w + delta_pos
            flag = False
            new_pos = 0
            if pos_wn > 0 and pos_wp < self.width:
                if len(pos_obs) > 0:
                    for item in pos_obs:
                        new_wn = item - obs_w - delta_pos
                        new_wp = item + obs_w + delta_pos
                        if pos < new_wn or pos > new_wp:
                            flag = True
                            new_pos = pos
                        else:
                            flag = False
                            new_pos = 0
                            break
                else:
                    new_pos = pos
                    flag = True
            if flag and new_pos > 0:
                pos_obs.append(new_pos)

        for i in range(n_ob):
            position = pos_obs[i]
            num = random_python.randint(0, 99999)
            if (num % 2) == 0:
                obstacle = ObstacleHotDog(x=position, y=self.height, height=obs_h, width=obs_w, id="hotdog")
            else:
                obstacle = ObstacleErvilha(x=position, y=self.height, height=obs_h, width=obs_w, id="ervilha")
            self.add_widget(obstacle, 2)
            self.obstacles.append(obstacle)

    def rain_collided(self, wid1, wid2):
        if wid2.x <= wid1.x + wid1.width and \
                wid2.x + wid2.width >= wid1.x and \
                wid2.y <= wid1.y + wid1.height and \
                wid2.y + wid2.height >= wid1.y:
            return True
        return False

    def rain_items(self, item_obj):
        collided = False
        fura = self.ids.furacao
        if self.rain_collided(fura, item_obj):
            collided = True
        # for obstacle in self.obstacles:
        #     if self.rain_collided(self.ids.furacao, obstacle):
        #         collided = True
        #         break
        return collided

    def rain_items_update(self, *args):
        collided = False
        for obstacle in self.obstacles:
            if self.rain_collided(self.ids.furacao, obstacle):
                if obstacle.id == "ervilha":
                    collided = True
                    break
        return collided


class GameOver(Screen):
    pass


class GamePontuacao(Screen):
    pass


class Obstacle(Widget):
    # color = ListProperty([0.3, 0.2, 0.2, 1])
    color = ListProperty([0.8, 0, 0, 1])
    scored = False
    gameScreen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim = Animation(x=-self.width, duration=3)
        self.anim.bind(on_complete=self.vanish)
        self.anim.start(self)
        self.gameScreen = App.get_running_app().root.get_screen('mario')

    def on_x(self, *args):
        if self.gameScreen:
            if self.x < self.gameScreen.ids.mario.x and not self.scored:
                self.gameScreen.score += 0.5
                self.scored = True

    def vanish(self, *args):
        self.gameScreen.remove_widget(self)
        self.gameScreen.obstacles.remove(self)


class ObstacleHotDog(Widget):
    scored = False
    gameScreen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim = Animation(y=-self.height, duration=t_animacao_furacao)
        self.anim.bind(on_complete=self.vanish)
        self.anim.start(self)
        self.gameScreen = App.get_running_app().root.get_screen('furacao')

    def on_y(self, *args):
        if self.gameScreen:
            fura = self.gameScreen.ids.furacao
            y_fura = fura.y + self.gameScreen.ids.furacao.height * 1.1
            if self.y <= y_fura and not self.scored:
                if self.gameScreen.rain_items(self):
                    tam = len(self.gameScreen.obstacles)
                    # self.gameScreen.score += 1 / tam
                    self.gameScreen.score += 1
                    self.scored = True

    def vanish(self, *args):
        self.gameScreen.remove_widget(self)
        self.gameScreen.obstacles.remove(self)


class ObstacleErvilha(Widget):
    scored = False
    gameScreen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim = Animation(y=-self.height, duration=t_animacao_furacao)
        self.anim.bind(on_complete=self.vanish)
        self.anim.start(self)
        self.gameScreen = App.get_running_app().root.get_screen('furacao')

    def on_y(self, *args):
        if self.gameScreen:
            fura = self.gameScreen.ids.furacao
            y_fura = fura.y + self.gameScreen.ids.furacao.height * 1.1
            if self.y <= y_fura and not self.scored:
                if self.gameScreen.rain_items(self):
                    self.gameScreen.game_over()
                    self.scored = True

    def vanish(self, *args):
        self.gameScreen.remove_widget(self)
        self.gameScreen.obstacles.remove(self)


class Player(Image):
    speed = NumericProperty(0)


class Star(Image):
    pass


class FuraCao(Image):
    speed = NumericProperty(0)


class HotDog(Image):
    pass


class Ervilha(Image):
    pass

class MarioBros(App):
    pass


MarioBros().run()


if __name__ == '__main__':
    MarioBros().run()
