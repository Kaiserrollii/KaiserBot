function All() {
  document.getElementById('master').innerHTML = MasterTable;
}

var DataTable = "<table id = 'DataTable'><tr class = 'header'>\
<th><div class = 'tabletitle'>Data</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.book <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Any type</div></span></div></td>";
    DataTable += "<td>Returns the novel that is the closet match to the specified query.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.read</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.charts <div class = 'tooltip'>[Artist]\
    <span class = 'tooltiptext'>[Artist]: Valid artist on the charts (see k.chart_ex for full list)</div></span></div></td>";
    DataTable += '<td>Returns the chart positions for the specified artist. Supports Melon, Flo, Bugs, genie, soribada,\
    and Naver. Artist name is case insensitive, but hangul names are often required.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.chart</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.define <div class = 'tooltip'>[Word]\
    <span class = 'tooltiptext'>Valid noun, verb, adjective, and/or adverb</div></span></div></td>";
    DataTable += "<td>Retrieves definitions of the specified word.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.def<br>k.word</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.melon <div class = 'tooltip'>[Timeframe]\
    <span class = 'tooltiptext'>Valid timeframe (see k.melon_ex for full list)</div></span></div></td>";
    DataTable += '<td>Returns the top ten songs on the Melon charts according to the specified timeframe.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.mel</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.movie <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Valid query</div></span></div></td>";
    DataTable += '<td>Returns the top search from IMDB.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.mov</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.pop <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Group / soloist / group member, etc.</div></span></div></td>";
    DataTable += "<td>Retrieves info on groups, soloists, companies, shows, albums, and singles. Information from Kpop Wiki.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.kpop</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.profile <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Valid group/soloist on Kprofiles</div></span></div></td>";
    DataTable += "<td>Retrieves info on any group or soloist.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.profile</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.reddit_controversial <div class = 'tooltip'>[Subreddit] [Timeframe]\
    <span class = 'tooltiptext'>[Subreddit]: Do <strong>not </strong>include 'r/'<br>[Timeframe]: must be a valid timeframe\
    (see k.rc_ex for full list)</div></span></div></td>";
    DataTable += '<td>Returns the most controversial post from an SFW subreddit according to the specified timeframe.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.rc</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.reddit_hot <div class = 'tooltip'>[Subreddit]\
    <span class = 'tooltiptext'>Do <strong>not</strong> include 'r/'</div></span></div></td>";
    DataTable += '<td>Retrieves the current hot post from an SFW subreddit.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.rh</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.reddit_new <div class = 'tooltip'>[Subreddit]\
    <span class = 'tooltiptext'>Do <strong>not </strong>include 'r/'</div></span></div></td>";
    DataTable += '<td>Returns the newest post from an SFW subreddit.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.rn</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.reddit_random <div class = 'tooltip'>[Subreddit]\
    <span class = 'tooltiptext'>Do <strong>not </strong>include 'r/'</div></span></div></td>";
    DataTable += '<td>Returns a random post from an SFW subreddit (within the past ~5 days of posts).</td>';
    DataTable += "<td><div class = 'tablealiases'>k.rr</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.reddit_top <div class = 'tooltip'>[Subreddit]\
    <span class = 'tooltiptext'>Do <strong>not</strong> include 'r/'</div></span></div></td>";
    DataTable += '<td>Retrieves the top post from an SFW subreddit according to the specified timeframe.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.rt</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.si <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Any type</div></span></div></td>";
    DataTable += "<td>Returns relevant kpop servers according to the specified query.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.ksi</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.steam <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Any type</div></span></div></td>";
    DataTable += "<td>Returns the most relevant Steam search result according to the specified query.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.game</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.stock <div class = 'tooltip'>[Ticker] [Timeframe]\
    <span class = 'tooltiptext'>[Ticker]: Valid ticker symbol<br>[Timeframe]: s/m/l</div></span></div></td>";
    DataTable += "<td>Retrieves closing price data of the specified equity within the specified timeframe and presents a graphical \
    representation of the data retrieved. \
    <a href = 'https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/StockInfo.md', target = '_blank', style = 'color: rgb(243, 136, 54)'>\
    <strong>Documentation.</strong></a></td>";
    DataTable += "<td><div class = 'tablealiases'>k.stonks</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.translate <div class = 'tooltip'>[Start]/[End] [Message]\
    <span class = 'tooltiptext'>[Start]: Valid language code<br>[End]: Valid language code<br>[Message]: Any type</div></span></div></td>";
    DataTable += "<td>Translates the message according to the specified language codes.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.tr</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.twitter_trends <div class = 'tooltip'>[Amount] [Location]\
    <span class = 'tooltiptext'>[Amount]: Integer from 1-25<br>[Location]: Valid location</div></span></div></td>";
    DataTable += "<td>Retrieves the specified amount of trending topics on Twitter in the specified location. \
    <a href = 'https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/WOEIDs.md', target = '_blank', style = 'color: rgb(243, 136, 54)'>\
    <strong>Documentation.</strong></a></td>";
    DataTable += "<td><div class = 'tablealiases'>k.twt</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.twitter_graph <div class = 'tooltip'>[Amount] [Location]\
    <span class = 'tooltiptext'>[Amount]: Integer from 1-25<br>[Location]: Valid location</div></span></div></td>";
    DataTable += "<td>Retrieves the specified amount of trending topics on Twitter in the specified location and presents a graphical \
    representation of the data retrieved. \
    <a href = 'https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/WOEIDs.md', target = '_blank', style = 'color: rgb(243, 136, 54)'>\
    <strong>Documentation.</strong></a></td>";
    DataTable += "<td><div class = 'tablealiases'>k.twg</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.twitter_search <div class = 'tooltip'>[Query] [Category] [Timeframe]\
    <span class = 'tooltiptext'>[Query]: Hashtag, single word, or multiple words. For multiple, add + between each.<br><br>\
    [Category]: popular/p or recent/r. If recent, leave timeframe blank.<br><br>\
    [Timeframe]: Integer between 0 - 7. Leave blank for recent.</div></span></div></td>";
    DataTable += '<td>Retrieves three tweets according to the specified query, category, and timeframe.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.tws</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.urban <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Any type</div></span></div></td>";
    DataTable += '<td>Returns the Urban Dictionary definition of the specified query.</td>';
    DataTable += "<td><div class = 'tablealiases'>k.urb</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.wotd</div></td>";
    DataTable += "<td>Returns the word of the day, courtesy of Merriam Webster.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.dailyword</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.youtube_search <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Valid YouTube search query</div></span></div></td>";
    DataTable += "<td>Returns the top five most relevant YouTube videos/channels/playlists of the specified query.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.yts</div></td></tr>";

    DataTable += "<tr><td><div class = 'tablecommands'>k.youtube_top <div class = 'tooltip'>[Query]\
    <span class = 'tooltiptext'>Valid YouTube search query</div></span></div></td>";
    DataTable += "<td>Returns the most relevant YouTube video of the specified query.</td>";
    DataTable += "<td><div class = 'tablealiases'>k.yt</div></td></tr>";

    DataTable += '</table>';

function Data() { 
  document.getElementById('MasterTable').innerHTML = DataTable;
}

var GamesTable = "<table id = 'GamesTable'><tr class = 'header'>\
<th><div class = 'tabletitle'>Games</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.advice <div class = 'tooltip'>[Question]\
    <span class = 'tooltiptext'>Any type</div></span> <i class = 'fa fa-commenting'></div></td>";
    GamesTable += '<td>Ask any question. Receive good advice.</td>';
    GamesTable += "<td><div class = 'tablealiases'>k.question</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.choose <div class = 'tooltip'>[Choice 1]...[Choice n]\
    <span class = 'tooltiptext'>[Choice n]: Any type</div></span></div></td>";
    GamesTable += '<td>Makes a choice for you.</td>';
    GamesTable += "<td><div class = 'tablealiases'>k.choice</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.cloutify <div class = 'tooltip'>[Message]\
    <span class = 'tooltiptext'>Any type</div></span></div></td>";
    GamesTable += '<td>Returns a cloutified version of the specified message.</td>';
    GamesTable += "<td><div class = 'tablealiases'>k.scramble<br>k.jumble</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.cringe <i class = 'fa fa-commenting'></td>";
    GamesTable += '<td>Returns something cringey.</td>';
    GamesTable += "<td><div class = 'tablealiases'>k.yikes</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.dice <div class = 'tooltip'>[n]\
    <span class = 'tooltiptext'>Positive integer</div></span></div></td>";
    GamesTable += '<td>Rolls an n-sided die.</td>';
    GamesTable += "<td><div class = 'tablealiases'>k.roll</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.hungergames <div class = 'tooltip'>[Category]\
    <span class = 'tooltiptext'>Male/female/mixed</div></span></div></td>";
    GamesTable += '<td>Runs a Hunger Games simulator.</td>';
    GamesTable += "<td><div class = 'tablealiases'>k.hg</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.magic8ball <div class = 'tooltip'>[Question]\
    <span class = 'tooltiptext'>Any type</div></span> <i class = 'fa fa-commenting'></div></td>";
    GamesTable += "<td>Ask any question, and it'll give an answer. May not be a good one, though.</td>";
    GamesTable += "<td><div class = 'tablealiases'>k.magic</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.ship <div class = 'tooltip'>[1] [2]\
    <span class = 'tooltiptext'>[1]: Any type<br>[2]: Any type</div></span> <i class = 'fa fa-commenting'></div></td>";
    GamesTable += '<td>Ship any two things together and find out their compatibility, as well as recommended next steps.</td>';
    GamesTable += "<td><div class = 'tablealiases'>k.compatibility</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.spongebobify <div class = 'tooltip'>[Message]\
    <span class = 'tooltiptext'>Any type</div></span></div></td>";
    GamesTable += "<td>Returns a spongebobified version of the specified message.</td>";
    GamesTable += "<td><div class = 'tablealiases'>k.copypasta</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.spongebobify2 <div class = 'tooltip'>[Message]\
    <span class = 'tooltiptext'>Any type</div></span></div></td>";
    GamesTable += "<td>Returns a scuffed spongebobified version of the specified message.</td>";
    GamesTable += "<td><div class = 'tablealiases'>k.scuffed</div></td></tr>";

    GamesTable += "<tr><td><div class = 'tablecommands'>k.uwufy <div class = 'tooltip'>[Message]\
    <span class = 'tooltiptext'>Any type</div></span></div></td>";
    GamesTable += '<td>Returns an uwufied version of the specified message.</td>';
    GamesTable += "<td><div class = 'tablealiases'>k.uwu</div></td></tr>";

    GamesTable += '</table>';

function Games() { 
  document.getElementById('MasterTable').innerHTML = GamesTable;
}

var ImagesTable = "<table id = 'ImagesTable'><tr class = 'header'>\
<th><div class = 'tabletitle'>Images</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>";

    ImagesTable += "<tr><td><div class = 'tablecommands'>k.img_analyze <div class = 'tooltip'>[Link]\
    <span class = 'tooltiptext'>[Link]: Valid image link</div></span></div></td>";
    ImagesTable += "<td>Returns an analysis of the specified image.</td>";
    ImagesTable += "<td><div class = 'tablealiases'>k.img_a</div></td></tr>";

    ImagesTable += "<tr><td><div class = 'tablecommands'>k.img_crop <div class = 'tooltip'>[Link] [Amount]\
    <span class = 'tooltiptext'>[Link]: Valid image link<br>[Amount]: Positive integer less than half the image width/height\
    </div></span></div></td>";
    ImagesTable += "<td>Returns a cropped version of the image with [amount] pixels removed from each side.</td>";
    ImagesTable += "<td><div class = 'tablealiases'>k.img_c</div></td></tr>";

    ImagesTable += "<tr><td><div class = 'tablecommands'>k.img_filter <div class = 'tooltip'>[Link] [Filter]\
    <span class = 'tooltiptext'>[Link]: Valid image link<br>[Filter]: Valid filter (see k.img_filter_ex)</div></span></div></td>";
    ImagesTable += "<td>Returns the image with the specified filter applied.</td>";
    ImagesTable += "<td><div class = 'tablealiases'>k.img_f</div></td></tr>";

    ImagesTable += "<tr><td><div class = 'tablecommands'>k.img_superimpose <div class = 'tooltip'>[Link1] [Link2]\
    <span class = 'tooltiptext'>[Link1]: Valid image link<br>[Link2]: Valid image link</div></span></div></td>";
    ImagesTable += "<td>Returns a superimposed version of the two specified images. Images may be of different sizes.</td>";
    ImagesTable += "<td><div class = 'tablealiases'>k.img_s</div></td></tr>";

    ImagesTable += "<tr><td><div class = 'tablecommands'>k.img_transform <div class = 'tooltip'>[Link] [Direction]\
    <span class = 'tooltiptext'>[Link]: Valid image link<br>[Direction]: Vertical/v or horizontal/h</div></span></div></td>";
    ImagesTable += "<td>Returns a flipped version of the image according to the specified direction.</td>";
    ImagesTable += "<td><div class = 'tablealiases'>k.img_t</div></td></tr>";

    ImagesTable += "<tr><td><div class = 'tablecommands'>k.img_wasted <div class = 'tooltip'>[Link]\
    <span class = 'tooltiptext'>[Link]: Valid image link</div></span></div></td>";
    ImagesTable += "<td>Returns a GTA V wasted version of the specified image.</td>";
    ImagesTable += "<td><div class = 'tablealiases'>k.img_w</div></td></tr>";

    ImagesTable += '</table>';

function Images() { 
  document.getElementById('MasterTable').innerHTML = ImagesTable;
}

var MathTable = "<table id = 'MathTable'><tr class = 'header'>\
<th><div class = 'tabletitle'>Math</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.area_ngon <div class = 'tooltip'>[n] [Radius]\
    <span class = 'tooltiptext'>[n]: Positive integer<br>[Radius]: Positive number </div></span></div></td>";
    MathTable += '<td>Calculates the area of an n-sided regular polygon with the specified radius.</td>';
    MathTable += "<td><div class = 'tablealiases'>k.ngon<br>k.area</div></td></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.bmi <div class = 'tooltip'>[Height] [Weight]\
    <span class = 'tooltiptext'>[Height]: Positive number (cm)<br>[Weight]: Positive number (kg)</div></span></div></td>";
    MathTable += '<td>Calculates BMI given height in cm and weight in kg.</td>';
    MathTable += "<td><div class = 'tablealiases'>k.BMI</div></td></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.cipher <div class = 'tooltip'>[Increment] [Message]\
    <span class = 'tooltiptext'>[Increment]: Integer<br>[Message]: Any type</div></span></div></td>";
    MathTable += '<td>Encrypts a message by shifting each character by the specified increment.</td>';
    MathTable += "<td><div class = 'tablealiases'>k.encrypt</td></div></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.convert <div class = 'tooltip'>[Temperature]\
    <span class = 'tooltiptext'>Number+[C or F]</div></span></div></td>";
    MathTable += "<td>Converts the specified temperature to either C or F.</td>";
    MathTable += "<td><div class = 'tablealiases'>k.conv</div></td></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.derivative <div class = 'tooltip'>[Variable] [Function]\
    <span class = 'tooltiptext'>[Variable]: Letter<br>[Function]: Valid function (follows BEDMAS)</div></span></div></td>";
    MathTable += '<td>Calculates the derivative of the function with respect to the given variable.</td>';
    MathTable += "<td><div class = 'tablealiases'>k.deriv<br>k.differentiate</div></td></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.evaluate <div class = 'tooltip'>[Expression]\
    <span class = 'tooltiptext'>Valid expression (follows BEDMAS)</div></span></div></td>";
    MathTable += "<td>Evaluates/simplifies any mathematical expression. Supports multiple variables.</td>";
    MathTable += "<td><div class = 'tablealiases'>k.eval<br>k.simplify</div></td></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.expand <div class = 'tooltip'>[Expression]\
    <span class = 'tooltiptext'>Valid expression (follows BEDMAS)</div></span></div></td>";
    MathTable += "<td>Expands any mathematical expression. Supports multiple variables.</td>";
    MathTable += "<td><div class = 'tablealiases'>k.exp</div></td></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.gcd <div class = 'tooltip'>[x] [y]\
    <span class = 'tooltiptext'>[x]: Integer<br>[y]: Integer</div></span></div></td>";
    MathTable += "<td>Consumes two integers, x and y, and returns their GCD.</td>";
    MathTable += "<td><div class = 'tablealiases'>k.GCD</div></td></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.integral <div class = 'tooltip'>[Variable] [Function]\
    <span class = 'tooltiptext'>[Variable]: Letter<br>[Function]: Valid function (follows BEDMAS)</div></span></div></td>";
    MathTable += '<td>Calculates the indefinite integral of the function with respect to the given variable.</td>';
    MathTable += "<td><div class = 'tablealiases'>k.int<br>k.integrate</div></td></tr>";

    MathTable += "<tr><td><div class = 'tablecommands'>k.limit <div class = 'tooltip'>[Variable] [Approaches] [Function]\
    <span class = 'tooltiptext'>[Variable]: Letter<br>[Approaches]: 'inf' for infinity<br>[Function]: Valid function (follows BEDMAS)\
    </div></span></div></td>";
    MathTable += '<td>Calculates the limit as the function approaches the specified value.</td>';
    MathTable += "<td><div class = 'tablealiases'>k.lim</div></td></tr>";

    

    

    MathTable += '</table>';

function Math() { 
  document.getElementById('MasterTable').innerHTML = MathTable;
}

var ModerationTable = "<table id = 'ModerationTable'><tr class = 'header'>\
<th><div class = 'tabletitle'>Moderation</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>";

    ModerationTable += "<tr><td><div class = 'tablecommands'>k.cleanse <div class = 'tooltip'>[Amount]\
    <span class = 'tooltiptext'>Positive integer</div></span></div></td>";
    ModerationTable += '<td>Deletes the specified amount of messages.</td>';
    ModerationTable += "<td><div class = 'tablealiases'>k.purge<br>k.clean</div></td>";
    ModerationTable += "<td><div class = 'tableperms'>Manage Messages</div></td></tr>";

    ModerationTable += "<tr><td><div class = 'tablecommands'>k.slowmode <div class = 'tooltip'>[Duration] [Units]\
    <span class = 'tooltiptext'>[Duration]: Positive integer<br>[Units]: sec/min/h<br>Stop: [k.slowmode off]\
    </div></span></div></td>";
    ModerationTable += '<td>Activates slowmode in the current channel according to the given duration.</td>';
    ModerationTable += "<td><div class = 'tablealiases'>k.slow<br>k.sm</div></td>";
    ModerationTable += "<td><div class = 'tableperms'>Manage Messages</div></td></tr>";

    ModerationTable += "<tr><td><div class = 'tablecommands'>k.mute <div class = 'tooltip'>[User]\
    <span class = 'tooltiptext'>@ or ID</div></span></div></td>";
    ModerationTable += '<td>Mutes the specified user.</td>';
    ModerationTable += "<td><div class = 'tablealiases'>k.shh</div></td>";
    ModerationTable += "<td><div class = 'tableperms'>Mute Members</div></td></tr>";

    ModerationTable += "<tr><td><div class = 'tablecommands'>k.unmute <div class = 'tooltip'>[User]\
    <span class = 'tooltiptext'>@ or ID</div></span></div></td>";
    ModerationTable += '<td>Unmutes the specified user.</td>';
    ModerationTable += "<td><div class = 'tablealiases'>k.reverseshh</div></td>";
    ModerationTable += "<td><div class = 'tableperms'>Mute Members</div></td></tr>";

    ModerationTable += "<tr><td><div class = 'tablecommands'>k.kick <div class = 'tooltip'>[User]\
    <span class = 'tooltiptext'>@ or ID</div></span></div></td>";
    ModerationTable += '<td>Kicks the specified user.</td>';
    ModerationTable += "<td><div class = 'tablealiases'>k.sadbye</div></td>";
    ModerationTable += "<td><div class = 'tableperms'>Kick Members</div></td></tr>";

    ModerationTable += "<tr><td><div class = 'tablecommands'>k.ban <div class = 'tooltip'>[User]\
    <span class = 'tooltiptext'>@ or ID</div></span></div></td>";
    ModerationTable += '<td>Bans the specified user.</td>';
    ModerationTable += "<td><div class = 'tablealiases'>k.CRIMINAL</div></td>";
    ModerationTable += "<td><div class = 'tableperms'>Ban Members</div></td></tr>";

    ModerationTable += "<tr><td><div class = 'tablecommands'>k.unban <div class = 'tooltip'>[User]\
    <span class = 'tooltiptext'>[Username][Tag]</div></span></div></td>";
    ModerationTable += '<td>Unbans the specified user.</td>';
    ModerationTable += "<td><div class = 'tablealiases'>k.reverseCRIMINAL</div></td>";
    ModerationTable += "<td><div class = 'tableperms'>Ban Members</div></td></tr>";

    ModerationTable += "<tr><td><div class = 'tablecommands'>k.say <div class = 'tooltip'>[Channel] [Message]\
    <span class = 'tooltiptext'>[Channel]: Valid channel<br>[Message]: Any type</div></span></div></td>";
    ModerationTable += '<td>Sends a message in the specified channel.</td>';
    ModerationTable += "<td><div class = 'tablealiases'>k.send</div></td>";
    ModerationTable += "<td><div class = 'tableperms'>Administrator</div></td></tr>";

    ModerationTable += '</table>';

function Moderation() { 
  document.getElementById('MasterTable').innerHTML = ModerationTable;
}

var MiscellaneousTable = "<table id = 'MiscellaneousTable'><tr class = 'header'>\
<th><div class = 'tabletitle'>Miscellaneous</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>\
<th><div class = 'tabletitle'>&#x200b;</div></th>";

    MiscellaneousTable += "<tr><td><div class = 'tablecommands'>k.avatar <div class = 'tooltip'>[User]\
    <span class = 'tooltiptext'>[User]: @ or ID<br>If empty, returns self</div></span></div></td>";
    MiscellaneousTable += "<td>Returns the avatar of the specified user.</td>";
    MiscellaneousTable += "<td><div class = 'tablealiases'>k.av<br>k.pfp<br>k.dp</div></td></tr>";

    MiscellaneousTable += "<tr><td><div class = 'tablecommands'>k.boticon</div></td>";
    MiscellaneousTable += '<td>Returns the KaiserBot icon.</td>';
    MiscellaneousTable += "<td><div class = 'tablealiases'>k.bot_icon</div></td></tr>";

    MiscellaneousTable += "<tr><td><div class = 'tablecommands'>k.help</div></td>";
    MiscellaneousTable += '<td>Returns a general help page for KaiserBot.</td>';
    MiscellaneousTable += "<td><div class = 'tablealiases'>k.pabo</div></td></tr>";

    MiscellaneousTable += "<tr><td><div class = 'tablecommands'>k.invite</div></td>";
    MiscellaneousTable += '<td>Returns an invite link to Kaisercord.</td>';
    MiscellaneousTable += "<td><div class = 'tablealiases'>k.inv</div></td></tr>";

    MiscellaneousTable += "<tr><td><div class = 'tablecommands'>k.patreon</div></td>";
    MiscellaneousTable += "<td>Returns the bot's patreon's page.</td>";
    MiscellaneousTable += "<td><div class = 'tablealiases'>k.simp</div></td></tr>";

    MiscellaneousTable += "<tr><td><div class = 'tablecommands'>k.ping</div></td>";
    MiscellaneousTable += "<td>Returns the bot's ping.</td>";
    MiscellaneousTable += "<td><div class = 'tablealiases'>k.pong</div></td></tr>";

    MiscellaneousTable += "<tr><td><div class = 'tablecommands'>k.servericon</div></td>";
    MiscellaneousTable += '<td>Returns the server icon.</td>';
    MiscellaneousTable += "<td><div class = 'tablealiases'>k.server_icon</div></td></tr>";

    MiscellaneousTable += "<tr><td><div class = 'tablecommands'>k.website</div></td>";
    MiscellaneousTable += "<td>Returns the bot's website.</td>";
    MiscellaneousTable += "<td><div class = 'tablealiases'>k.site</div></td></tr>";

    MiscellaneousTable += '</table>';

function Miscellaneous() { 
  document.getElementById('MasterTable').innerHTML = MiscellaneousTable;
}

// Currently broken even though it was working perfectly fine before
// Will fix later

// function flashingdownarrow() {
//   var a;
//   a = document.getElementById('downarrow');
//   a.innerHTML = '&#xf107;';
//   setTimeout(function () {
//       a.innerHTML = '&#x200b;';
//     }, 1000);
// }
// flashingdownarrow();
// setInterval(flashingdownarrow, 2000);

function Search() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById('searchbutton');
  filter = input.value.toUpperCase();
  table = document.getElementById('MasterTable');
  tr = table.getElementsByTagName('tr');
  
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName('td')[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = '';
      } else {
        tr[i].style.display = 'none';
      }
    }       
  }
}

function opensidenavbar() {
  document.getElementById('sidenavbar').style.width = '250px';
  document.getElementById('main').style.marginLeft = '250px';
}

function closesidenavbar() {
  document.getElementById('sidenavbar').style.width = '0';
  document.getElementById('main').style.marginLeft= '0';
}

function darkmode() {
  var bodyclass = document.body;
  bodyclass.classList.toggle('darkmode_body');
  
  var changelogcontentclass = document.getElementsByClassName('changelog_content'),
    i, len;
for(i = 0, len = changelogcontentclass.length; i < len; i++){
    changelogcontentclass[i].classList.toggle('darkmode_changelog_content');
}
  var footerbodyclass = document.getElementsByClassName('footerbody'),
    i, len;
for(i = 0, len = footerbodyclass.length; i < len; i++){
  footerbodyclass[i].classList.toggle('darkmode_footer_body');
}
  var colourboxclass = document.getElementsByClassName('colourbox'),
  i, len;
for(i = 0, len = colourboxclass.length; i < len; i++){
    colourboxclass[i].classList.toggle('darkmode_colourbox');
}
  var sidenavclass = document.getElementsByClassName('sidenav'),
      i, len;
    for(i = 0, len = sidenavclass.length; i < len; i++){
        sidenavclass[i].classList.toggle('darkmode_sidenav');
}
  var tooltipchangelogtextclass = document.getElementsByClassName('tooltipchangelogtext'),
        i, len;
    for(i = 0, len = tooltipchangelogtextclass.length; i < len; i++){
      tooltipchangelogtextclass[i].classList.toggle('darkmode_tooltipchangelogtext');
}
}
