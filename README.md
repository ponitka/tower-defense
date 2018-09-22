# tower-defense
Implemented in Python 3 using GTK+ library with graphics made by myself. <br />
Player needs to build towers to prevent bots from reaching their destination which <br />
changes over time. Board is a randomly generated maze. <br />

Game rules and controls:
<ul>
  <li>Usage of towers: WASD for moving, Q for buying, arrows for changing.</li>
  <li>New wave comes every 15 seconds. You'll lose when your budget becomes negative.</li>
  <li>By killing an enemy you earn 1$, by letting an enemy reach the star you lose 2$.</li>
  <li>Towers attributes include (in that order): range, speed and cost</li>
</ul>

To start the game run <code>main.py</code> in Python 3 (<code>$ python3 main.py</code>)
