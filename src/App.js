import React, { Component, createContext } from 'react';
import ReactDOM from 'react-dom';
import Game from './Game';
import AIPlayer from './AIPlayer';

class WebPlayer {
  constructor() {
    this.my_turn = false;

  }

  on_init(width, height, turn) {
  }

  on_my_turn(game) {
    this.my_turn = true;
    this.game = game;
    console.log("web player turn!");
    ReactDOM.render(<App />, document.getElementById('root'));

  }

  onClickCell(x, y) {
     
  }
}

const web_player = new WebPlayer();
const game = new Game(15, 15, web_player, new AIPlayer());
const Context = createContext();

class App extends Component {
  render() {
    return <Board />;
  }
}

class Cell extends Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    if(this.props.game.turn === 1){
      if(this.props.game.move(this.props.col, this.props.row) == 0) {
	var game_tmp = this.props.game;
        setTimeout(function() { 
	  return game_tmp.play_the_game();}, 0)
	console.log("handle click");
      }
    }
    this.forceUpdate();
  }

  render() {
    return <button onClick={this.handleClick}>
   {this.props.game.get_state(this.props.col,this.props.row)}</button>;
  }
}

class Row extends Component {
  render() {
    var cells = [];
    for (var i = 0; i < 15; i++) {
      cells.push(<Cell game={this.props.game} col={i} row={this.props.row}/>);
    }
    return (<div style={{display: 'flex'}}> {cells} </div>);
  }
}


class Board extends Component {
  constructor(props) {
    super(props);
    this.state = {game: game};
  }

  render() {
    var rows = [];
    for (var i = 0; i < 15; i++) {
      rows.push(<Row game={this.state.game} row={i}/>);
    }
    return (rows);
  }
}

export default App;
