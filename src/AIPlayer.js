class AIPlayer {
  on_init(width, height, turn) {
    this.width = width;
    this.height = height;
    this.turn = turn;
  }

  on_my_turn(game) {
    game.move(parseInt(Math.random() * this.width),parseInt(Math.random() * this.height));
    setTimeout(function() {return game.play_the_game();}, 0);
  }
}

export default AIPlayer;
