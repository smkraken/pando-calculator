#Imports
import kivy #Kivy 1.10.1
from kivy.app import App

from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.factory import Factory

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty
#End Imports

#Global Functions
def is_digit(var):
    return var.isdigit()

def get_num(varstr):
    s = ""
    if varstr[0] == '-':
        s += "-"
        varstr = varstr[1:]
    for c in varstr:
        if not is_digit(c) and c != '.':
            break
        s += c
    return(float(s), len(s))

def perform_operation(st,stack):
    print(stack)
    i = stack.index(st)
    n2 = stack.pop(i+1)
    n1 = stack.pop(i-1)
    if st == '^':   stack[i-1] = n1 ** n2
    elif st == '*': stack[i-1] = n1 * n2
    elif st == '/': stack[i-1] = n1 / n2
    elif st == '+': stack[i-1] = n1 + n2
    elif st == '-': stack[i-1] = n1 - n2

    print("{} {} {} = {}".format(n1,st,n2,stack[i-1]))

def eval_math_expr(expr):

    n, end_n = get_num(expr)
    expr_list = [n]
    expr = expr[end_n:]

    while expr:
        expr_list.append(expr[0])
        expr = expr[1:]
        n, end_n = get_num(expr)
        expr_list.append(n)
        expr = expr[end_n:]

    while len(expr_list) > 1:
        if '^' in expr_list:
            perform_operation('^',expr_list)

        else:
            if '*' in expr_list: perform_operation('*',expr_list)
            elif '/' in expr_list: perform_operation('/',expr_list)

            else:
                if '+' in expr_list:  perform_operation('+',expr_list)
                elif '-' in expr_list: perform_operation('-',expr_list)

    output = expr_list[0]
    return str(output)

#Button Classes
class Btn(Button):
    def __init__(self, **kwargs):
        super(Btn,self).__init__(**kwargs)
        self.font_size = self.height * 2 / 3

    __events__ = ('on_long_press', )

    long_press_time = Factory.NumericProperty(1)

    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_press(self):
        self.parent.parent.parent.ids.calc_input.text += self.text

    def on_long_press(self, *largs):
        pass

class SpecialBtns(Btn):
    def __init__(self, **kwargs):
        super(SpecialBtns,self).__init__(**kwargs)

    def on_press(self):
        if self.text is '=':
            self.parent.parent.parent.calculate()

        elif self.text is 'del':
            self.parent.parent.parent.ids.calc_input.text = self.parent.parent.parent.ids.calc_input.text[:-1]

    def on_long_press(self):
        if self.text is 'del':
            self.parent.parent.parent.ids.calc_input.text = ''

class EqWindow(TextInput):
    def __init__(self, **kwargs):
        super(EqWindow,self).__init__(**kwargs)
        self.font_size = self.height
        self.size_hint = 1, 0.2
        self.multiline = False
        self.padding = [10, self.height / 4, 10, 10]

class InterfaceLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(InterfaceLayout, self).__init__(**kwargs)

        number_grid = GridLayout(cols=3)
        for i in range(10):
            number_grid.add_widget(Btn(text = str(i)))
        number_grid.add_widget(Btn(text = '.'))
        number_grid.add_widget(SpecialBtns(text = '='))

        operator_grid = GridLayout(rows = 5)
        operator_grid.add_widget(SpecialBtns(text = 'del',))
        for i in '+-/*':
            operator_grid.add_widget(Btn(text = str(i)))


        self.add_widget(number_grid)
        self.add_widget(operator_grid)
        number_grid.size_hint = 0.8, 1
        operator_grid.size_hint = 0.2, 1

class CalculatorWidget(GridLayout):

    def calculate(self, *args):
        input = self.ids.calc_input.text
        output = eval_math_expr(input)
        self.ids.calc_input.text = str(output)

class CalcApp(App):
  def build(self):
      root = CalculatorWidget()
      return root

if __name__ == "__main__":
    interactive = True
    if interactive:
        CalcApp().run()
    else:
        eval_math_expr('1^3-3*2/2+2')
        eval_math_expr('2.0^3*10/2-45+2')
