import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from highlight_text import HighlightText, ax_text, fig_text

#Importing the Font Manager from mplsoccer & loading the fonts
from mplsoccer import FontManager
font_normal = FontManager(("https://github.com/googlefonts/rubik/blob/main/fonts/ttf/Rubik-Light.ttf?raw=true"))
font_regular = FontManager(("https://github.com/googlefonts/rubik/blob/main/fonts/ttf/Rubik-Regular.ttf?raw=true"))
font_bold = FontManager(("https://github.com/googlefonts/rubik/blob/main/fonts/ttf/Rubik-Bold.ttf?raw=true"))

#Loading the files. 
df=pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRJj4AGUbgivmk97VuyKh930RsJj73mKrvYEMCMyQSZD4B8ZXSsE2luVHGpi_SovSkiIkwhSFcB0I3V/pub?gid=1192983856&single=true&output=csv')
standard=pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSvpLX4C_XPuAowHS9qQuhfY6cdAcOKW0QUK_n0pVqFCPuyXa3bKdxlejpyGAmg9j6yUpUHpFzZU0x9/pub?gid=1674956316&single=true&output=csv')
passing= pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSp9baBbmntRr9gVCSrpCrwjJkQIIyD1-m61xm_tZnBrXeCDV2txiHs9YuIaTvrJw/pub?gid=1839356204&single=true&output=csv')
pass_types= pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTt-FtJb8qnmwcXUSsphI-Kg9HqZYhI1H6NLKPN4xY5jGYfIvb96BD_zl6Xh0A_LeZ1EIOe8nMtBb8S/pub?gid=847414082&single=true&output=csv')
sca= pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTdzGrNxOFnenlG4ws9I9Ll4KRilrr4TcTEKvqJUDG30KBXfn1qa2j5MFvCHiM8XUISchcVBgvG2S5Q/pub?gid=1301766462&single=true&output=csv')
dfa= pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTnqfWVkyxDwc9BefQK5pnQvNAAh7I69_SXrl6Fty68f_P7u84bnKvtNJaIzwlnS4G4DDJux5_MGHXs/pub?gid=977595461&single=true&output=csv')
poss=pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQaeL7--7aoBkdXMHzJhJLcrd9jths9KPV4B4G8IXKNfRecrUUKx_wCRnPDDqMES_vtDxWAgH1ISbm_/pub?gid=394498778&single=true&output=csv')
Misc=pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vREVH3BhIYWTBLiCiIA79XrKthzPAZLMxtSW8l6WPjW64UtK5w4f6rO3sw6kB0J9hoYTND_AdTQAFR6/pub?gid=864059211&single=true&output=csv')
shooting=pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTFzS1reLqaAguoKsY0ce1-DV0Ogs2-EvihAwd11JxfcydjSTC8LSBJXm4D12zWvLSLfXzBxzAe9R-Y/pub?gid=2010219322&single=true&output=csv')
df=df[df['New Positions']!='Goalkeeper']
df=df.drop(['Unnamed: 0'], axis=1)
df=df.reset_index(drop=True)
standard=standard[['Player','Squad','npxG','xA']]
shooting=shooting[['Player','Squad','Sh']]
passing=passing[['Player','Squad','TAtt','TCmp%','LAtt', 'LCmp%','KP', 'Final3rd', 'PPA','Prog' ]]
pass_types=pass_types[['Player','Squad','Sw','Press']]
poss=poss[['Player', 'Squad','DAtt','CProg','C3rd','CCPA']]
dfa=dfa[['Player','Squad','TklW','Int','Blocks','Clr','Succ']]
dfa['Blocks + Clearances']= dfa['Blocks']+dfa['Clr']
Misc=Misc[['Player', 'Squad','Recov','Won']]
sca=sca[['Player','Squad','SCA90']]
df= pd.merge(df,standard, on=['Player','Squad'],how='left')
df= pd.merge(df,pass_types, on=['Player','Squad'],how='left')
df= pd.merge(df,sca, on=['Player','Squad'],how='left')
df= pd.merge(df,dfa, on=['Player','Squad'],how='left')
df= pd.merge(df,poss, on=['Player','Squad'],how='left')
df= pd.merge(df,Misc, on=['Player','Squad'],how='left')
df= pd.merge(df,shooting, on=['Player','Squad'],how='left')
df= pd.merge(df,passing, on=['Player','Squad'],how='left')
DA= df[['Player','TklW','Succ','Int','Recov','Won','Blocks + Clearances']]
GCC= df[['Player','npxG','xA','Sh','DAtt', 'SCA90','KP']]
BP= df[['Player','Prog','CProg','Final3rd','C3rd','PPA','CCPA' ]]
BD=df[['Player','TAtt','TCmp%','LAtt','LCmp%','Sw','Press']]

import streamlit as st

st.write("""
      # Player Scouting Dashboard """ )
st.write("""
      ##### based on percentile ranks """ )
competition= st.selectbox("Select a Competition", (df['Comp'].unique()))
dff= df[df['Comp']==competition]
squad= st.selectbox("Select a Club", (dff['Squad'].unique()))
dff=dff[dff['Squad']== squad]
position= st.selectbox("Select a Position", (dff['New Positions'].unique()))
dff=dff[dff['New Positions']== position]

df=df[df['New Positions']==position]
df=df.reset_index(drop=True)
DA= df[['Player','TklW','Succ','Int','Recov','Won','Blocks + Clearances']]
GCC= df[['Player','npxG','xA','Sh','DAtt', 'SCA90','KP']]
BP= df[['Player','Prog','CProg','Final3rd','C3rd','PPA','CCPA' ]]
BD=df[['Player','TAtt','TCmp%','LAtt','LCmp%','Sw','Press']]

def scouting_bar(player):
    # def scouting_bar(competition,team,position,player)
    # select=[competition,team,position,player]
    select = [player]

    # df_1=df[df['Comp']== select[0]]
    # df_1=df_1[df_1['Squad']== select[1]]
    # df_1=df_1[df_1['New Positions']== select[2]]

    # df_1= df_1.reset_index(drop=True)

    for i in range(0, len(df)):
        if (df['Player'][i] == select[0]):
            j = i
            break
        else:
            continue

    # set up gridspec figure
    fig = plt.figure(figsize=(58.5, 58.5), constrained_layout=True)
    gs = fig.add_gridspec(nrows=13, ncols=13)

    # For Goal Contribution & Creativity
    ax2 = fig.add_subplot(gs[5:8, 0:5])
    df1 = pd.DataFrame({'Attributes': ['npxG', 'xA', 'Shots', 'Att. Dribbles', 'SCA', 'Key Passes'],
                        'Percentile': [round(stats.percentileofscore(GCC['npxG'], GCC['npxG'][j])),
                                       round(stats.percentileofscore(GCC['xA'], GCC['xA'][j])),
                                       round(stats.percentileofscore(GCC['Sh'], GCC['Sh'][j])),
                                       round(stats.percentileofscore(GCC['DAtt'], GCC['DAtt'][j])),
                                       round(stats.percentileofscore(GCC['SCA90'], GCC['SCA90'][j])),
                                       round(stats.percentileofscore(GCC['KP'], GCC['KP'][j]))]})

    df1['default'] = 100 - df1['Percentile']
    colors = ['blue', 'silver']
    df1.plot(x='Attributes', kind='barh', ax=ax2,
             stacked=True, legend=False, width=0.8,
             color=colors, xticks=np.arange(0, 110, 10), xlabel=' ', fontsize=40,
             mark_right=False)

    ax2.text(20, 6.5, 'Goal Contributions & Creativity', va='center', ha='left', fontsize=60, color="black", zorder=1,
             weight="bold", fontproperties=font_bold.prop)

    Values = [GCC['npxG'][j], GCC['xA'][j], GCC['Sh'][j], GCC['DAtt'][j], GCC['SCA90'][j], GCC['KP'][j]]
    k = 0
    # Add annotation to bars
    for i in ax2.patches:
        if (k <= 5):
            plt.text(i.get_width() + 0.2, i.get_y() + 0.35,
                     round(Values[k], 2),
                     fontsize=30, fontweight='bold',
                     color='black')
            k = k + 1

        elif (k == 6):
            break

    plt.axvline(50, color='black', ls='--', lw=1)
    # Remove x, y Ticks
    ax2.yaxis.set_ticks_position('none')

    # Editing the axis,spines & ticks
    ax2.spines['bottom'].set_color('black')
    ax2.spines['left'].set_color('black')
    ax2.spines['top'].set_color('grey')
    ax2.spines['right'].set_color('grey')
    ax2.spines['bottom'].set_linewidth(1)
    ax2.spines['left'].set_linewidth(1)
    ax2.spines['right'].set_linewidth(1)
    ax2.spines['top'].set_linewidth(1)

    ax2.text(51, -0.57, "Median", color="black", size="20", weight="normal")
    ax2.text(50, -1.4, "Percentile", color="black", size="30", weight="normal")
    ax2.text(-40.5, -2.50, "*npxG: Non-Penalty Expected Goals, xA:Expected Assists, SCA: Shot Creating Actions",
             color="black", size="33", weight="normal")

    # For Defensive Ability
    ax3 = fig.add_subplot(gs[5:8, 8:])
    df2 = pd.DataFrame({'Attributes': ['Succ. Tackles', 'Pressure Regains', 'Interceptions', 'Recoveries',
                                       'Aerials Won', 'Blocks + \n Clearances'],
                        'Percentile': [round(stats.percentileofscore(DA['TklW'], DA['TklW'][j])),
                                       round(stats.percentileofscore(DA['Succ'], DA['Succ'][j])),
                                       round(stats.percentileofscore(DA['Int'], DA['Int'][j])),
                                       round(stats.percentileofscore(DA['Recov'], DA['Recov'][j])),
                                       round(stats.percentileofscore(DA['Won'], DA['Won'][j])),
                                       round(stats.percentileofscore(DA['Blocks + Clearances'],
                                                                     DA['Blocks + Clearances'][j]))]})

    df2['default'] = 100 - df2['Percentile']
    colors = ['blue', 'silver']
    df2.plot(x='Attributes', kind='barh', ax=ax3,
             stacked=True, legend=False, width=0.8,
             color=colors, xticks=np.arange(0, 110, 10), xlabel=' ', fontsize=40,
             mark_right=False)

    ax3.text(27, 6.5, 'Defensive Ability', va='center', ha='left', fontsize=60, color="black", zorder=1, weight="bold",
             fontproperties=font_bold.prop)

    Values = [DA['TklW'][j], DA['Succ'][j], DA['Int'][j], DA['Recov'][j], DA['Won'][j], DA['Blocks + Clearances'][j]]
    k = 0
    # Add annotation to bars
    for i in ax3.patches:
        if (k <= 5):
            plt.text(i.get_width() + 0.2, i.get_y() + 0.35,
                     round(Values[k], 2),
                     fontsize=30, fontweight='bold',
                     color='black')
            k = k + 1
        elif (k == 6):
            break

    plt.axvline(50, color='black', ls='--', lw=1)
    # Remove x, y Ticks
    ax3.yaxis.set_ticks_position('none')

    # Editing the axis,spines & ticks
    ax3.spines['bottom'].set_color('black')
    ax3.spines['left'].set_color('black')
    ax3.spines['top'].set_color('black')
    ax3.spines['right'].set_color('black')
    ax3.spines['bottom'].set_linewidth(1)
    ax3.spines['left'].set_linewidth(1)
    ax3.spines['right'].set_linewidth(1)
    ax3.spines['top'].set_linewidth(1)

    ax3.text(51, -0.57, "Median", color="black", size="20", weight="normal")
    ax3.text(50, -1.4, "Percentile", color="black", size="30", weight="normal")

    # For Ball Progression & Build Up
    ax4 = fig.add_subplot(gs[10:, 0:5])
    df3 = pd.DataFrame({'Attributes': ['Progressive Passes', 'Progressive Carries', 'Final third \n Passes',
                                       'Final third \n carries', 'Passes into \nPA', 'Carries into\nPA'],
                        'Percentile': [round(stats.percentileofscore(BP['Prog'], BP['Prog'][j])),
                                       round(stats.percentileofscore(BP['CProg'], BP['CProg'][j])),
                                       round(stats.percentileofscore(BP['Final3rd'], BP['Final3rd'][j])),
                                       round(stats.percentileofscore(BP['C3rd'], BP['C3rd'][j])),
                                       round(stats.percentileofscore(BP['PPA'], BP['PPA'][j])),
                                       round(stats.percentileofscore(BP['CCPA'], BP['CCPA'][j]))]})

    df3['default'] = 100 - df3['Percentile']
    colors = ['blue', 'silver']
    df3.plot(x='Attributes', kind='barh', ax=ax4,
             stacked=True, legend=False, width=0.8,
             color=colors, xticks=np.arange(0, 110, 10), xlabel=' ', fontsize=40,
             mark_right=False)

    ax4.text(22, 6.5, 'Ball Progression & Build-up', va='center', ha='left', fontsize=60, color="black", zorder=1,
             weight="bold", fontproperties=font_bold.prop)

    Values = [BP['Prog'][j], BP['CProg'][j], BP['Final3rd'][j], BP['C3rd'][j], BP['PPA'][j], BP['CCPA'][j]]
    k = 0
    # Add annotation to bars
    for i in ax4.patches:
        if (k <= 5):
            plt.text(i.get_width() + 0.2, i.get_y() + 0.35,
                     round(Values[k], 2),
                     fontsize=30, fontweight='bold',
                     color='black')
            k = k + 1

        elif (k == 6):
            break

    plt.axvline(50, color='black', ls='--', lw=1)
    # Remove x, y Ticks
    ax4.yaxis.set_ticks_position('none')

    # Editing the axis,spines & ticks
    ax4.spines['bottom'].set_color('black')
    ax4.spines['left'].set_color('black')
    ax4.spines['top'].set_color('grey')
    ax4.spines['right'].set_color('grey')
    ax4.spines['bottom'].set_linewidth(1)
    ax4.spines['left'].set_linewidth(1)
    ax4.spines['right'].set_linewidth(1)
    ax4.spines['top'].set_linewidth(1)

    ax4.text(51, -0.57, "Median", color="black", size="20", weight="normal")
    ax4.text(50, -1.4, "Percentile", color="black", size="30", weight="normal")
    ax4.text(-40.5, -2.50, "*PA:Penalty Area", color="black", size="33", weight="normal")

    # For Passing & Ball Distribution
    ax5 = fig.add_subplot(gs[10:, 8:])
    df4 = pd.DataFrame({'Attributes': ['Attempted Passes', 'Pass Completion %', 'Att. Long Balls',
                                       'Long Ball Succ. Rate', 'Switch Passes', 'Passes Under Pressure'],
                        'Percentile': [round(stats.percentileofscore(BD['TAtt'], BD['TAtt'][j])),
                                       round(stats.percentileofscore(BD['TCmp%'], BD['TCmp%'][j])),
                                       round(stats.percentileofscore(BD['LAtt'], BD['LAtt'][j])),
                                       round(stats.percentileofscore(BD['LCmp%'], BD['LCmp%'][j])),
                                       round(stats.percentileofscore(BD['Sw'], BD['Sw'][j])),
                                       round(stats.percentileofscore(BD['Press'], BD['Press'][j]))]})

    df4['default'] = 100 - df4['Percentile']
    colors = ['blue', 'silver']
    df4.plot(x='Attributes', kind='barh', ax=ax5,
             stacked=True, legend=False, width=0.8,
             color=colors, xticks=np.arange(0, 110, 10), xlabel=' ', fontsize=40,
             mark_right=False)

    ax5.text(22, 6.5, 'Passing & Ball Distribution', va='center', ha='left', fontsize=60, color="black", zorder=1,
             weight="bold", fontproperties=font_bold.prop)

    Values = [BD['TAtt'][j], BD['TCmp%'][j], BD['LAtt'][j], BD['LCmp%'][j], BD['Sw'][j], BD['Press'][j]]
    k = 0
    # Add annotation to bars
    for i in ax5.patches:
        if (k <= 5):
            plt.text(i.get_width() + 0.2, i.get_y() + 0.35,
                     round(Values[k], 2),
                     fontsize=30, fontweight='bold',
                     color='black')
            k = k + 1

        elif (k == 6):
            break

    plt.axvline(50, color='black', ls='--', lw=1)
    # Remove x, y Ticks
    ax5.yaxis.set_ticks_position('none')

    # Editing the axis,spines & ticks
    ax5.spines['bottom'].set_color('black')
    ax5.spines['left'].set_color('black')
    ax5.spines['top'].set_color('black')
    ax5.spines['right'].set_color('black')
    ax5.spines['bottom'].set_linewidth(1)
    ax5.spines['left'].set_linewidth(1)
    ax5.spines['right'].set_linewidth(1)
    ax5.spines['top'].set_linewidth(1)

    ax5.text(51, -0.57, "Median", color="black", size="20", weight="normal")
    ax5.text(50, -1.4, "Percentile", color="black", size="30", weight="normal")

    # For the Name, Minutes Played, Team
    ax1 = fig.add_subplot(gs[0:3, :])
    # You can either create a HighlightText object
    HighlightText(x=0.30, y=0.80,
                  s=f"<{df['Player'][j].upper()} >" + ' <21-22 SEASON>',
                  highlight_textprops=[{"color": 'blue', 'size': 80},
                                       {"color": 'black', 'size': 80}], fontproperties=font_bold.prop,
                  ax=ax1)

    # ax1.text(0.25,0.75,df['Player'][4].upper() +' 21-22 SEASON',color="blue",size="60",fontproperties=font_bold.prop)

    HighlightText(x=0.30, y=0.55,
                  s=f"<Mins: >" + f"<{str(df['Min'][j])}>",
                  highlight_textprops=[{"color": 'black', 'size': 50},
                                       {"color": 'blue', 'size': 50}], fontproperties=font_bold.prop,
                  ax=ax1)

    # ax1.text(0.30,0.46,'Mins: '+ str(df['Min'][4]),color="black",size="35",fontproperties=font_bold.prop)
    HighlightText(x=0.55, y=0.55,
                  s=f"<Team: >" + f"<{df['Squad'][j]}>",
                  highlight_textprops=[{"color": 'black', 'size': 50},
                                       {"color": 'blue', 'size': 50}], fontproperties=font_bold.prop,
                  ax=ax1)

    # ax1.text(0.55,0.46,'Team: '+ df['Squad'][4],color="black",size="35",fontproperties=font_bold.prop)

    HighlightText(x=0.30, y=0.43,
                  s=f"<Pos: >" + f"<{df['New Positions'][j]}>",
                  highlight_textprops=[{"color": 'black', 'size': 50},
                                       {"color": 'blue', 'size': 50}], fontproperties=font_bold.prop,
                  ax=ax1)

    # ax1.text(0.30,0.32,'Pos: '+ df['New Positions'][4],color="black",size="35",fontproperties=font_bold.prop)

    HighlightText(x=0.55, y=0.43,
                  s=f"<Age: >" + f"<{str(round(df['Age'][j]))}>",
                  highlight_textprops=[{"color": 'black', 'size': 50},
                                       {"color": 'blue', 'size': 50}], fontproperties=font_bold.prop,
                  ax=ax1)

    # ax1.text(0.55,0.32,'Age: '+ str(round(df['Age'][4])),color="black",size="35",fontproperties=font_bold.prop)
    ax1.text(0.0097, 0.1,
             '*Percentile Rank vs Top-Five League ' + df['New Positions'][j] + 's with at least 1000 minutes played',
             color="black", size="35", weight="normal", style='italic')
    ax1.text(0.0097, 0.03, '*bar annotations are values /90', color="black", size="35", weight="normal", style='italic')
    ax1.text(0.88, 0.05, 'Data: FBref/Statsbomb', color="black", size="33", fontproperties=font_regular.prop,
             weight="bold")
    ax1.yaxis.set_ticks_position('none')
    ax1.xaxis.set_ticks_position('none')

    ax1.axes.xaxis.set_visible(False)
    ax1.axes.yaxis.set_visible(False)

    ax1.spines['bottom'].set_color('black')
    ax1.spines['left'].set_color('black')
    ax1.spines['top'].set_color('black')
    ax1.spines['right'].set_color('black')
    ax1.spines['bottom'].set_linewidth(4)
    ax1.spines['left'].set_linewidth(4)
    ax1.spines['right'].set_linewidth(4)
    ax1.spines['top'].set_linewidth(4)

    rect = plt.Rectangle(
        # (lower-left corner), width, height
        (0.0, 0.05), 0.95, 0.6, fill=False, color="k", lw=2,
        zorder=1000, transform=fig.transFigure, figure=fig
    )
    rect1 = plt.Rectangle(
        # (lower-left corner), width, height
        (0.0, 0.05), 0.95, 0.3, fill=False, color="k", lw=2,
        zorder=1000, transform=fig.transFigure, figure=fig
    )

    rect2 = plt.Rectangle(
        # (lower-left corner), width, height
        (0.0, 0.05), 0.475, 0.6, fill=False, color="k", lw=2,
        zorder=1000, transform=fig.transFigure, figure=fig
    )
    
    fig.patches.extend([rect])
    fig.patches.extend([rect1])
    fig.patches.extend([rect2])



import streamlit as st

#st.write("""
      # Player Scouting Dashboard """ )
#st.write("""
      ##### based on percentile ranks """ )
#competition= st.selectbox("Select a Competition", (df['Comp'].unique()))
#dff= df[df['Comp']==competition]
#squad= st.selectbox("Select a Club", (dff['Squad'].unique()))
#dff=dff[dff['Squad']== squad]
#position= st.selectbox("Select a Position", (dff['New Positions'].unique()))
#dff=dff[dff['New Positions']== position]
player1= st.selectbox("Select a Player", (dff['Player'].unique()))
print(player1)
                        
#st.write("""
      # Player Scouting Dashboard """ )


#scouting_bar(player1)
fig=scouting_bar(player1)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(fig)
     
