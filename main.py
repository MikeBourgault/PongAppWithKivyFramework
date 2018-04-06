from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.instructions import InstructionGroup, ContextInstruction, VertexInstruction


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    scorelimit = 10

    def btn_startmenu(self):
        self.ball.stop(self)

    def endgame(self):
        self.ball.stop(self)

    def serve_ball(self):
        randx = randint(0,11)
        randy = randint(0,11)
        vel = (randx,randy)
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, scorelimit):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # score left or right
        if self.ball.x < self.x:
            self.player2.score += 1
            if self.player2.score >= scorelimit:
                self.endgame()
            else:
                self.serve_ball()
        if self.ball.x > self.width:
            self.player1.score += 1
            if self.player2.score >= scorelimit:
                self.endgame()
            else:
                self.serve_ball()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

class PongBall(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def stop(self):
        pass

class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class StartMenu(BoxLayout):
    ball = ObjectProperty(PongBall)
    game = ObjectProperty(PongGame)

    def btn_resume(self):
        self.ball.move(self)
    def btn_restart(self):
        self.game.serve_ball(self)
    def btn_quit(self):
        pass

if __name__ == '__main__':
    PongApp().run()