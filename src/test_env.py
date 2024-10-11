import importlib
import game


class myAgent:
    def __init__(self) -> None:
        pass

    def move(self, observation, action_space):
        action = action_space.sample()
        return action


importlib.reload(game)
figs = []
env = game.Game()
print(env.observation_space.shape)
print(env.action_space.n)
my_agent = myAgent()
observation = env.reset(seed=42)
figs.append(env.render())
done = False

while not done:
    action = my_agent.move(observation, env.action_space)
    observation, reward, done, info = env.step(action)
    figs.append(env.render())
    # if env.game_turn == 20:
    #     break

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation

# Supposons que tu as une liste de figures stockées dans `figs`
# Chaque figure représente une étape du jeu

# Création de la figure principale
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Ajustement pour le slider en bas

# Affichage initial de la première figure
current_step = 0
img = ax.imshow(figs[current_step])  # Affiche la première figure

# Configuration du slider
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor="lightgoldenrodyellow")
slider = Slider(ax_slider, "Step", 0, len(figs) - 1, valinit=current_step)


# Fonction pour mettre à jour l'image selon la valeur du slider
def update(val):
    current_step = int(slider.val)
    img.set_data(figs[current_step])
    fig.canvas.draw_idle()


slider.on_changed(update)

plt.show()
