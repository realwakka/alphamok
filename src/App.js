import React, { Component, createContext } from 'react';
import Game from './Game';

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
	  console.log("asdf"); 
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
    this.state = {game: new Game(15,15)};
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
