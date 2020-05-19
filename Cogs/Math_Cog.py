import discord
import random 
import math
import sympy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from fractions import Fraction
from discord.ext import commands 


class Math_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Math: Online')

    # Consumes a valid expression consisting of operators, numbers, and/or variables.
    # Returns the evaluated expression 
    @commands.command(aliases = ['Evaluate', 'eval', 'Eval', 'simplify', 'Simplify'])
    async def evaluate(self, ctx, *, expression):
        parseable = expression.replace('^', '**').replace(' ', '')
        parsed = parse_expr(parseable)
        evaluated = str(simplify(parsed)).replace('**', '^')
        if evaluated == 'zoo' or evaluated == 'nan':
            await ctx.send('Unable to evaluate/simplify. Try again, and this time with a proper expression, pabo.')
        else:
            L = list(filter(lambda x: x.isalpha(), list(evaluated)))
            if L == []:
                evaluated = float(sum(Fraction(s) for s in evaluated.split()))
                await ctx.send(f''':question:: Evaluate/simplify `{expression}` ?\n'''
                        f':pencil:: `{evaluated}`')
            else:
                await ctx.send(f''':question:: Evaluate/simplify `{expression}` ?\n'''
                        f':pencil:: `{evaluated}`')

    @commands.command(aliases = ['Evaluate_ex', 'eval_ex', 'Eval_ex'])
    async def evaluate_ex(self, ctx):
        await ctx.send('```k.evaluate ((1 + 2) * 3)^2\n>>> 81\n\nk.evaluate x^3 / (4.34 - 2*x)\n>>> -x^3/(2*x - 4.34)```')

    # Consumes a valid expression consisting of operators, numbers, and/or variables
    # Returns the expanded expression 
    @commands.command(aliases = ['Expand', 'exp', 'Exp'])
    async def expand(self, ctx, *, expression):
        parseable = expression.replace('^', '**')
        parsed = parse_expr(parseable)
        expanded = str(expand(parsed)).replace('**', '^')
        await ctx.send(f''':question:: Expand `{expression}` ?\n'''
                       f':pencil:: `{expanded}`')

    @commands.command(aliases = ['Expand_ex', 'exp_ex', 'Exp_ex'])
    async def expand_ex(self, ctx):
        await ctx.send('```k.expand (x + 1)^2\n>>> x^2 + 2*x + 1```')

    # Consumes a nat, sides, and a positive num, radius
    # Returns the area of a regular polygon with [sides] sides and [radius] radius
    @commands.command(aliases = ['ngon', 'Ngon', 'area'])
    async def area_ngon(self, ctx, sides, radius):
            sides = abs(float(sides))
            radius = abs(float(radius))
            area = (sides * (radius ** 2) * math.sin((2 * math.pi) / sides)) / 2
            await ctx.send(f''':question:: Area of a regular **{sides}**-sided polygon with radius **{radius}** units?
:pencil:: `{area}` square units.''')

    @commands.command(aliases = ['ngon_ex', 'Ngon_ex', 'area_ex'])
    async def area_ngon_ex(self, ctx):
        await ctx.send('```k.area_ngon 5 10\n>>> 237.76412907378838```')

    # Consumes positive nums, height and weight
    # Returns BMI calculated from given height and weight (Reminder: BMI is not an accurate indicator of health)
    @commands.command(aliases = ['BMI'])
    async def bmi(self, ctx, height, weight):
        height = abs(float(height)) / 100
        weight = abs(float(weight))
        bmi = weight / (height ** 2)
        if bmi < 18:
            await ctx.send(f'Your BMI is **{bmi}**, which means you are classed as underweight. :sushi: :thumbsup:')
        elif bmi < 25:
            await ctx.send(f'Your BMI is **{bmi}**, which means you are classed as healthy. :thumbsup:')
        elif bmi < 30:
            await ctx.send(f'Your BMI is **{bmi}**, which means you are classed as overweight. :sushi: :thumbsdown:')
        elif bmi < 40:
            await ctx.send(f'Your BMI is **{bmi}**, which means you are classed as obese. :sushi: :thumbsdown: :thumbsdown:')
        else:
            await ctx.send(f'Your BMI is **{bmi}**, which means you are classed as morbidly obese. :sushi: :thumbsdown: :thumbsdown: :thumbsdown:')

    @commands.command(aliases = ['BMI_ex'])
    async def bmi_ex(self, ctx):
        await ctx.send('```k.bmi 180 70\n>>> 21.604938271604937```')

    # Consumes a str, message, and an int, increment
    # Returns the encrypted message by shifting each character by the specified increment
    @commands.command(aliases = ['Cipher', 'encrypt', 'Encrypt'])
    async def cipher(self, ctx, increment, *, message):
        increment = int(round(float(increment)))
        if increment == 0:
            await ctx.send(message)
        else:
            cipher = ''
            for char in message: 
                if char == ' ':
                    cipher = cipher + char
                elif char.isupper():
                    cipher = cipher + chr((ord(char) + increment - 65) % 26 + 65)
                else:
                    cipher = cipher + chr((ord(char) + increment - 97) % 26 + 97)
            await ctx.send(cipher)

    @commands.command(aliases = ['Cipher_ex', 'encrypt_ex', 'Encrypt_ex'])
    async def cipher_ex(self, ctx):
        await ctx.send('```k.cipher 1 stfu\n>>> tugv\n\nk.cipher 5 stan Irene\n>>> xyfs Nwjsj```')

    # Consumes a letter, variable, and a function. The variable used in the function must be consistent with the variable parameter.
    # Returns the derivative of the specified function
    @commands.command(aliases = ['Derivative', 'deriv', 'Deriv', 'differentiate', 'Differentiate'])
    async def derivative(self, ctx, variable, *, function):
        parseable = function.replace('^', '**').replace(' ', '')
        parsed = parse_expr(parseable)
        variable = parse_expr(variable)
        deriv = str(diff(parsed, variable)).replace('**', '^')
        if deriv.startswith('Derivative'):
            await ctx.send(f'Derivative of `{function}` is too complicated for me to calculate, nerd. Try again with a simpler function.')
        else:
            await ctx.send(f''':question:: Derivative of `{function}` with respect to `{variable}` ?\n'''
                           f':pencil:: `{deriv}`')

    @commands.command(aliases = ['Derivative_ex', 'deriv_ex', 'Deriv_ex', 'differentiate_ex', 'Differentiate_ex'])
    async def derivative_ex(self, ctx):
        await ctx.send('```k.derivative x 5*x\n>>> 5\n\nk.derivative y cos(y^2) / (4 + y)\n>>> -2*y*sin(y^2)/(y + 4) - cos(y^2)/(y + 4)^2```')

    # Consumes a str, variable, and a function. The variable used in the function must be consistent with the variable parameter.
    # Returns the integral of the specified function
    @commands.command(aliases = ['Integral', 'int', 'Int', 'integrate', 'Integrate'])
    async def integral(self, ctx, variable, *, function):
        parseable = function.replace('^', '**').replace(' ', '')
        parsed = parse_expr(parseable)
        variable = parse_expr(variable)
        integral = str(integrate(parsed, variable)).replace('**', '^')
        if integral.startswith('Integral'):
            await ctx.send(f'Integral of `{function}` is too complicated for me to calculate, nerd. Try again with a simpler function.')
        else:
            await ctx.send(f''':question:: Integral of `{function}` with respect to `{variable}` ?\n'''
                           f':pencil:: `{integral}`')

    @commands.command(aliases = ['Integral_ex', 'int_ex', 'Int_ex', 'integrate_ex', 'Integrate_ex'])
    async def integral_ex(self, ctx):
        await ctx.send('```k.integral x 2*x\n>>> x^2\n\nk.integral y (4 - 8 * y)^3\n>>> -128*y^4 + 256*y^3 - 192*y^2 + 64*y```')

    # Consumes a str, variable, a num/str approaches, and a function. The variable used in the function must be consistent with the variable parameter.
    # Returns the limit as the specified function approaches [approaches]
    @commands.command(aliases = ['Limit', 'lim', 'Lim'])
    async def limit(self, ctx, variable, approaches, *, function):
        parseable = function.replace('^', '**').replace(' ', '')
        parseable2 = approaches.replace('inf', 'oo')
        parsed = parse_expr(parseable)
        parsed2 = parse_expr(parseable2)
        variable = parse_expr(variable)
        lim = str(limit(parsed, variable, parsed2)).replace('**', '^')
        lim = lim.replace('oo', 'inf')
        if lim.startswith('Limit'):
            await ctx.send(f'Limit of `{function}` is too complicated for me to calculate, nerd. Try again with a simpler function.')
        if lim.startswith('AccumBounds'):
            lim = lim[5:11] + ': ' + lim[11:]
            await ctx.send(f''':question:: Limit as `{function}` approaches `{approaches}` ?\n'''
                           f':pencil:: `{lim}`')
        else:
            await ctx.send(f''':question:: Limit as `{function}` approaches `{approaches}` ?\n'''
                           f':pencil:: `{lim}`')

    @commands.command(aliases = ['Limit_ex', 'lim_ex', 'Lim_ex'])
    async def limit_ex(self, ctx):
        await ctx.send('```k.limit x 5 1/x\n>>> 1/5\n\nk.limit y inf sin(y)\n>>> Bounds: (-1, 1)```')

    # Consumes one and two, which must be integers
    # Returns the GCD of the specified integers
    @commands.command(aliases = ['GCD', 'Gcd'])
    async def gcd(self, ctx, one, two):
        one = int(round(float(one)))
        two = int(round(float(two)))
        gcd = math.gcd(one, two)
        await ctx.send(f''':question:: GCD of **{one}** and **{two}**?\n'''
                       f':pencil:: `{gcd}`')

    @commands.command(aliases = ['GCD_ex', 'Gcd_ex'])
    async def gcd_ex(self, ctx):
        await ctx.send('```k.gcd 8 52\n>>> 4```')


def setup(bot):
    bot.add_cog(Math_Cog(bot))
