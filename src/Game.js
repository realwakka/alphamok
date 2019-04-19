var events = require('events');

function check(game, x, y, front, back) {
  let state = game.get_state(x, y);

  let check_tmp = (game, fx, fy, func, state) => {
    let count = 0;

    do {
      count++;
      [fx, fy] = func(fx, fy);
    } while (game.get_state(fx,fy) === state);
    return count;
  }
  let total_count = check_tmp(game, x, y, back, state) + check_tmp(game, x, y, front, state);
  console.log("total : " + total_count);
  if (total_count === 6) {
    return true;
  } else {
    return false;
  }
}

function check_finish(game, x, y) {
  if (check(game, x, y, (x, y) => { return [x+1, y]; }, (x, y) => { return [x-1, y]; }))
    return true;

  if (check(game, x, y, (x, y) => { return [x, y+1]; }, (x, y) => { return [x, y-1]; }))
    return true;

  if (check(game, x, y, (x, y) => { return [x+1, y+1]; }, (x, y) => { return [x-1, y-1]; }))
    return true;

  if (check(game, x, y, (x, y) => { return [x+1, y-1]; }, (x, y) => { return [x-1, y+1]; }))
    return true;

  return false;
}

class Game {
  constructor(width, height, player1, player2) {
    this.board_state = [];
    this.width = width;
    this.height = height;

    this.player1 = player1;
    this.player2 = player2;

    this.initialize();
  }

  initialize() {
    this.board_state = [];
    for (var i = 0; i < this.width * this.height; i++)
      this.board_state.push(0);
    this.turn = 1;

    this.player1.on_init(this.width, this.height, 1);

    this.player2.on_init(this.width, this.height, 2);
    this.event_emitter = new events.EventEmitter();

    this.event_emitter.on("play", this.play_the_game);
  }

  get_state(x, y) {
    if (x >= 0 && x < this.width && y >= 0 && y < this.height) {
      return this.board_state[y * this.width + x];
    } else {
      return -1;
    }
  }

  move(x, y) {
    if (this.get_state(x,y) === 0) {
      this.board_state[y * this.width + x] = this.turn;

      if (check_finish(this, x,y)) {
	window.alert("FINISHED!!!");
	this.initialize();
	return this.turn + 2;
      }

      return 0;
    } else {
      return -1;
    }
  }

  swap_turn() {
    if(this.turn === 1) {
      this.turn = 2;
    } else {
      this.turn = 1;
    }
  }

  check_finish(x, y) {
    return check_finish(this, x, y);    
  }

  play_the_game() {
    console.log(this);
    this.swap_turn();
    console.log("play_the_game!");
    if (this.turn === 1) {
      this.player1.on_my_turn(this);
    } else {
      this.player2.on_my_turn(this);
    }
  }
}

export default Game;
