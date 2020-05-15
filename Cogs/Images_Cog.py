import discord
import datetime 
import asyncio
import pandas as pd
import numpy as np
import io
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageStat, ImageEnhance, ImageChops, ImageOps, ImageFilter
from discord.ext import commands 


class Images_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Images: Online')

    # Consumes link, which must be a valid image link
    # Returns an analysis of the specified image
    @commands.command(aliases = ['Img_analyze', 'img_analyse', 'Img_analyse', 'img_stats','Img_stats', 'img_stat', 'Img_stat', 'img_a', 'Img_a'])
    async def img_analyze(self, ctx, link):
        if 'https://' not in link:
            await ctx.send('Your image must be a valid image link, pabo. Try again.')
        else:
            pull = requests.get(link)
            img = Image.open(BytesIO(pull.content))

            embed = discord.Embed(title = 'Image Analysis', color = discord.Colour(0xefe61))
            embed.set_thumbnail(url = link)
            embed.add_field(name ='General information:', value = f'{img.format}, **{img.size[0]}** x **{img.size[1]}**, {img.mode}', inline = False)
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = f'{ctx.guild.icon_url}')
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed)

    @commands.command(aliases = ['Img_analyze_ex', 'img_analyse_ex', 'Img_analyse_ex', 'img_stats_ex', 'Img_stats_ex', 'img_stat_ex', 'Img_stat_ex',
    'img_a_ex', 'Img_a_ex'])
    async def img_analyze_ex(self, ctx):
        await ctx.send('```k.img_analyze https://cdn.discordapp.com/attachments/665437935088304132/707679455371460668/Kaiser.png\n\n\
>>> [Analysis of Kaiser.png]```')

    # Consumes link, which must be a valid image link, and amount, which must be a positive integer less than half the image width/height
    # Returns a cropped version of the image
    @commands.command(aliases = ['Img_crop', 'img_cut', 'Img_cut', 'img_cropper', 'Img_cropper', 'img_c', 'Img_c'])
    async def img_crop(self, ctx, link, amount):
        if 'https://' not in link:
            await ctx.send('Your image must be a valid image link, pabo. Try again.')
        else:
            pull = requests.get(link)
            imgcrop = Image.open(BytesIO(pull.content))
            width = imgcrop.size[0]
            height = imgcrop.size[1]
            amount = int(round(float(amount)))

            if amount >= (width / 2) or amount >= (height / 2) or amount <= 0:
                await ctx.send("You can't crop out the *entire* image, pabo. I suggest you run `k.img_analyze [Link]` before trying to crop.")
            else:
                ImageOps.crop(imgcrop, border = amount).save('Images/imgcrop.png')
                with open('Images/imgcrop.png', 'rb') as f: file = BytesIO(f.read())
                imgcrop = discord.File(file, filename = 'imgcrop.png')

                embed = discord.Embed(title = 'Image Crop', color = discord.Colour(0xefe61),
                description = f'Original: **{width}** x **{height}**\nCropped: **{width - amount * 2}** x **{height - amount * 2}**')
                embed.set_thumbnail(url = link)
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
                icon_url = f'{ctx.guild.icon_url}')
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_image(url = f'attachment://imgcrop.png')

                message = await ctx.send('*Cropping image...*')
                await asyncio.sleep(2)
                await message.edit(content = '*Cropping image... ✅*')
                await asyncio.sleep(1)
                await ctx.send(file = imgcrop, embed = embed)
                await message.delete()

    @commands.command(aliases = ['Img_crop_ex', 'img_cut_ex', 'Img_cut_ex', 'img_cropper_ex', 'Img_cropper_ex', 'img_c_ex', 'Img_c_ex'])
    async def img_crop_ex(self, ctx):
        await ctx.send("```Please don't spam this command. If nothing is returned after ~20 seconds, it's safe to assume either the bot is \
overloaded or something else has gone wrong.\n\n\
k.img_crop https://cdn.discordapp.com/attachments/665437935088304132/707679455371460668/Kaiser.png 100\n\n\
>>> [Cropped version of Kaiser.png with 100px removed from the borders (all four sides)]```")

    # Consumes link, which must be a valid image link, and direction, which must be either vertical or horizontal
    # Returns a flipped version of the image according to the specified direction
    @commands.command(aliases = ['Img_transform', 'img_flip', 'Img_flip', 'img_t', 'Img_t'])
    async def img_transform(self, ctx, link, direction):
        if 'https://' not in link:
            await ctx.send('Your image must be a valid image link, pabo. Try again.')
        else:
            pull = requests.get(link)
            imgtransform = Image.open(BytesIO(pull.content))
            direction = direction.lower()

            if direction == 'vertical' or direction == 'v':
                direction = 'Vertical Flip'
                ImageOps.flip(imgtransform).save('Images/imgtransform.png')
                with open('Images/imgtransform.png', 'rb') as f: file = BytesIO(f.read())
                imgtransform = discord.File(file, filename = 'imgtransform.png')
            elif direction == 'horizontal' or direction == 'h':
                direction = 'Horizontal Flip'
                ImageOps.mirror(imgtransform).save('Images/imgtransform.png')
                with open('Images/imgtransform.png', 'rb') as f: file = BytesIO(f.read())
                imgtransform = discord.File(file, filename = 'imgtransform.png')
            else:
                await ctx.send('Direction must be either `vertical` / `v` or `horizontal` / `h`, pabo. Try again.')
                return
        
            embed = discord.Embed(title = 'Image Transform', color = discord.Colour(0xefe61), description = f'Transformation: **{direction}**')
            embed.set_thumbnail(url = link)
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = f'{ctx.guild.icon_url}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_image(url = f'attachment://imgtransform.png')

            message = await ctx.send('*Transforming image...*')
            await asyncio.sleep(2)
            await message.edit(content = '*Transforming image... ✅*')
            await asyncio.sleep(1)
            await ctx.send(file = imgtransform, embed = embed)
            await message.delete()

    @commands.command(aliases = ['Img_transform_ex', 'img_flip_ex', 'Img_flip_ex', 'img_t_ex', 'Img_t_ex'])
    async def img_transform_ex(self, ctx):
        await ctx.send("```Please don't spam this command. If nothing is returned after ~20 seconds, it's safe to assume either the bot is \
overloaded or something else has gone wrong.\n\n\
k.img_transform https://cdn.discordapp.com/attachments/665437935088304132/707679455371460668/Kaiser.png horizontal\n\n\
>>> [Transformed version of Kaiser.png flipped horizontally]```")

    # Consumes link, which must be a valid image link, and filt, which must be a valid filter (see k.img_filter_ex for full list)
    # Returns the image with the specified filter applied
    @commands.command(aliases = ['Img_filter', 'img_effect', 'Img_effect', 'img_f', 'Img_f'])
    async def img_filter(self, ctx, link, filt):
        if 'https://' not in link:
            await ctx.send('Your image must be a valid image link, pabo. Try again.')
        else:
            pull = requests.get(link)
            imgfilter = Image.open(BytesIO(pull.content))
            filt = filt.lower()

            if filt == 'blur' or filt == 'b':
                filt = 'Blur'
                imgfilter.filter(ImageFilter.BLUR).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'black&white' or filt == 'b&w' or filt == 'bw':
                filt = 'Black & White'
                ImageEnhance.Color(imgfilter).enhance(0.0).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'contour' or filt == 'c':
                filt = 'Contour'
                imgfilter.filter(ImageFilter.CONTOUR).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'detail' or filt == 'd':
                filt = 'Detail'
                imgfilter.filter(ImageFilter.DETAIL).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'edge_enhance' or filt == 'ee':
                filt = 'Edge Enhance'
                imgfilter.filter(ImageFilter.EDGE_ENHANCE).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'edge_enhance++' or filt == 'ee++':
                filt = 'Edge Enhance ++'
                imgfilter.filter(ImageFilter.EDGE_ENHANCE_MORE).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'emboss' or filt == 'em':
                filt = 'Emboss'
                imgfilter.filter(ImageFilter.EMBOSS).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'smooth' or filt == 'sm':
                filt = 'Smooth'
                imgfilter.filter(ImageFilter.SMOOTH).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'smooth++' or filt == 'sm++':
                filt = 'Smooth ++'
                imgfilter.filter(ImageFilter.SMOOTH_MORE).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            elif filt == 'sharpen' or filt == 'sharp' or filt == 'sh':
                filt = 'Sharpen'
                imgfilter.filter(ImageFilter.SHARPEN).save('Images/imgfilter.png')
                with open('Images/imgfilter.png', 'rb') as f: file = BytesIO(f.read())
                imgfilter = discord.File(file, filename = 'imgfilter.png')
            else:
                await ctx.send("That's not a valid filter, pabo. The full filter list can be found at `k.img_filter_ex`.")
                return
            
            embed = discord.Embed(title = 'Image Filter', color = discord.Colour(0xefe61), description = f'Filter: **{filt}**')
            embed.set_thumbnail(url = link)
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = f'{ctx.guild.icon_url}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_image(url = f'attachment://imgfilter.png')

            message = await ctx.send('*Applying filter to image...*')
            await asyncio.sleep(2)
            await message.edit(content = '*Applying filter to image... ✅*')
            await asyncio.sleep(1)
            await ctx.send(file = imgfilter, embed = embed)
            await message.delete()

    @commands.command(aliases = ['Img_filter_ex', 'img_effect_ex', 'Img_effect_ex', 'img_f_ex', 'Img_f_ex'])
    async def img_filter_ex(self, ctx):
        d = {'Filter': ['Blur', 'Black&White', 'Contour', 'Detail', 'Edge_Enhance', 'Edge_Enhance++', 'Emboss', 'Smooth', 'Smooth++', 'Sharpen'], 
                 'Alias': ['b', 'b&w', 'c', 'd', 'ee', 'ee++', 'em', 'sm', 'sm++', 'sh']}
        index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        df = pd.DataFrame(data = d, index = index)

        await ctx.send(f"```Please don't spam this command. If nothing is returned after ~30 seconds, it's safe to assume either the bot is \
overloaded or something else has gone wrong.\n\nFull list of filters:\n\n{df}\n\n\
k.img_filter https://cdn.discordapp.com/attachments/665437935088304132/707679455371460668/Kaiser.png Sharpen\n\n\
>>> [Enhanced version of Kaiser.png with a sharpen filter applied]```")

    # Consumes link1 and link2, which must be valid image links. Images may be of different sizes.
    # Returns a superimposed version of the two images
    @commands.command(aliases = ['Img_superimpose', 'img_super', 'Img_super', 'img_s', 'Img_s'])
    async def img_superimpose(self, ctx, link1, link2):
        if ('https://' not in link1) and ('https:// not in link2'):
            await ctx.send('Your image must be a valid image link, pabo. Try again.')
        else:
            pull1 = requests.get(link1)
            imgsuperimpose1 = Image.open(BytesIO(pull1.content)).convert('RGBA')
            pull2 = requests.get(link2)
            imgsuperimpose2 = Image.open(BytesIO(pull2.content)).convert('RGBA')

            ImageChops.multiply(imgsuperimpose1, imgsuperimpose2).save('Images/imgsuperimpose.png')
            with open('Images/imgsuperimpose.png', 'rb') as f: file = BytesIO(f.read())
            imgsuperimpose = discord.File(file, filename = 'imgsuperimpose.png')

            embed = discord.Embed(title = 'Image Superimpose', color = discord.Colour(0xefe61),
            description = f'Image 1: {link1}\nImage 2: {link2}')
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = f'{ctx.guild.icon_url}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_image(url = f'attachment://imgsuperimpose.png')

            message = await ctx.send('*Superimposing images...*')
            await asyncio.sleep(3)
            await message.edit(content = '*Superimposing images... ✅*')
            await asyncio.sleep(1)
            await ctx.send(file = imgsuperimpose, embed = embed)
            await message.delete()

    @commands.command(aliases = ['Img_superimpose_ex', 'img_super_ex', 'Img_super_ex', 'img_s_ex', 'Img_s_ex'])
    async def img_superimpose_ex(self, ctx):
        await ctx.send("```Please don't spam this command. If nothing is returned after ~30 seconds, it's safe to assume either the bot is \
overloaded or something else has gone wrong.\n\n\
k.img_superimpose https://cdn.discordapp.com/attachments/665437935088304132/707679455371460668/Kaiser.png \
https://cdn.discordapp.com/attachments/665437935088304132/707717245224222760/KaiserBot.png\n\n\
>>> [Superimposed version of the two images]```")

    # Consumes link, which must be a valid image link
    # Returns a wasted version of the specified image
    @commands.command(aliases = ['Img_wasted', 'img_w', 'Img_w'])
    async def img_wasted(self, ctx, link):
        if 'https://' not in link:
            await ctx.send('Your image must be a valid image link, pabo. Try again.')
        else:
            pull = requests.get(link)
            imgwasted = Image.open(BytesIO(pull.content)).convert('RGBA')

            TINT_COLOR = (0, 0, 0) 
            TRANSPARENCY = .50  
            OPACITY = int(round(float(255 * TRANSPARENCY)))

            width = imgwasted.size[0]
            height = imgwasted.size[1]
            heightposition = int(round(float(height / 2)))
            heightincrement = int(round(float(height * 0.08)))
            fontsize = int(round(float((heightincrement * 2) / 3 * 2)))
            fontincrement = int(round(float(fontsize / 7)))
            textfont = ImageFont.truetype("Images/GTA.ttf", fontsize)
            textwidth = textfont.getsize('Wasted')[0]
            textheight = textfont.getsize('Wasted')[1]
            xout = int(round(float((width - textwidth) / 2)))
            yout = int(round(float((height - textheight - fontincrement) / 2)))
            outincrement = fontsize // 24

            overlay = Image.new('RGBA', imgwasted.size, TINT_COLOR + (0,))
            draw = ImageDraw.Draw(overlay) 
            draw.rectangle(((0, heightposition + heightincrement), (width, heightposition - heightincrement)), fill = TINT_COLOR + (OPACITY,))
            draw.text((xout - outincrement, yout - outincrement), 'Wasted', font = textfont, fill = 'black')
            draw.text((xout + outincrement, yout - outincrement), 'Wasted', font = textfont, fill = 'black')
            draw.text((xout - outincrement, yout + outincrement), 'Wasted', font = textfont, fill = 'black')
            draw.text((xout + outincrement, yout + outincrement), 'Wasted', font = textfont, fill = 'black')
            draw.text((xout, yout), 'Wasted', fill = '#F72C28', font = textfont)

            imgwasted = ImageEnhance.Color(imgwasted).enhance(0.0)
            imgwasted = ImageEnhance.Brightness(imgwasted).enhance(1.5)
            imgwasted = imgwasted.filter(ImageFilter.BLUR)
            imgwasted = Image.alpha_composite(imgwasted, overlay)
            imgwasted.save('Images/imgwasted.png')
            with open('Images/imgwasted.png', 'rb') as f: file = BytesIO(f.read())
            imgwasted = discord.File(file, filename = 'imgwasted.png')

            embed = discord.Embed(title = 'Image Wastedifier', color = discord.Colour(0xefe61), description = '*Press F to pay respects.*')
            embed.set_thumbnail(url = link)
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = f'{ctx.guild.icon_url}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_image(url = f'attachment://imgwasted.png')

            message = await ctx.send('*Wastedifying image...*')
            await asyncio.sleep(3)
            await message.edit(content = '*Wastedifying image... ✅*')
            await asyncio.sleep(1)
            embedmessage = await ctx.send(file = imgwasted, embed = embed)
            await message.delete()
            await embedmessage.add_reaction('🇫')

    @commands.command(aliases = ['Img_wasted_ex', 'img_w_ex', 'Img_w_ex'])
    async def img_wasted_ex(self, ctx):
        await ctx.send("```Please don't spam this command. If nothing is returned after ~30 seconds, it's safe to assume either the bot is \
overloaded or something else has gone wrong.\n\n\
k.img_wasted https://cdn.discordapp.com/attachments/665437935088304132/707679455371460668/Kaiser.png\n>>> [Wasted version of Kaiser.png]\n\n\
Struggle: https://imgur.com/a/zvVVSgX```")


    # In development
    # @commands.command()
    # async def img_write(self, ctx, link, font, colour, *, text):
    #     if 'https://' not in link:
    #         await ctx.send('Your image must be a valid image link, pabo. Try again.')
    #     else:
    #         font = str(font).lower()
    #         if font == 'regular' or font == 're':
    #             textfont = ImageFont.truetype("Images/Regular.ttf", 16)
    #         elif font == 'comicsans' or font == 'c':
    #             textfont = ImageFont.truetype("Images/ComicSans.ttf", 16)
    #         elif font == 'fancy' or font == 'f':
    #             textfont = ImageFont.truetype("Images/Fancy.ttf", 16)
    #         elif font == 'horror' or font == 'h':
    #             textfont = ImageFont.truetype("Images/Horror.ttf", 16)
    #         elif font == 'rool2' or font == 'ro':
    #             textfont = ImageFont.truetype("Images/rool2.ttf", 16)
    #         else:
    #             await ctx.send("That's not a valid font, pabo. The full font list can be found at `k.img_write_ex`.")
    #             return

    #         pull = requests.get(link)
    #         imgwrite = Image.open(BytesIO(pull.content))
    #         imgwidth = imgwrite.size[0]
    #         imgheight = imgwrite.size[1]

    #         draw = ImageDraw.Draw(imgwrite)
    #         textwidth = textfont.getsize(text)[0]
    #         textheight = textfont.getsize(text)[1]
    #         draw.text(((imgheight - textwidth) / 2, (imgheight - textheight) / 2), text, fill = colour, font = textfont)

    #         imgwrite.save('Images/imgwrite.png')
    #         with open('Images/imgwrite.png', 'rb') as f: file = BytesIO(f.read())
    #         imgwrite = discord.File(file, filename = 'imgwrite.png')

    #         await ctx.send(file = imgwrite)


def setup(bot):
    bot.add_cog(Images_Cog(bot))
