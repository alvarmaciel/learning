#! /bin/bash

if [[ $1 == "test" ]]
then
  PSQL="psql --username=postgres --dbname=worldcuptest -t --no-align -c"
else
  PSQL="psql --username=freecodecamp --dbname=worldcup -t --no-align -c"
fi

# Do not change code above this line. Use the PSQL variable above to query your database.

echo $($PSQL "TRUNCATE games, teams")

cat games.csv | while IFS="," read YEAR ROUND WINNER OPPONENT WINNER_GOALS OPPONENT_GOALS
do
    if [[ $YEAR != "year" ]]
    then
       echo try "$YEAR |$ROUND | $WINNER | $OPPONENT | $WINNER_GOALS| $OPPONENT_GOALS"
        # get game_id
        GAME_ID=$($PSQL "SELECT game_id FROM games WHERE year='$YEAR' AND round='$ROUND' AND winner_id IS NOT NULL AND opponent_id IS NOT NULL and winner_goals='$WINNER_GOALS' AND opponent_goals='$OPPONENT_GOALS'")
        # if not game IDfound
        if [[ -z $GAME_ID ]]
        then
            # get team WINNER id
            TEAM_WINNER_ID=$($PSQL "SELECT team_id FROM teams WHERE name='$WINNER'")
            # if team_id not found
            if [[ -z $TEAM_WINNER_ID ]]
            then
                # insert team WINNER
                INSERT_WINNER_RESULT=$($PSQL "INSERT INTO teams(name) VALUES('$WINNER')")
                echo $INSERT_WINNER_RESULT
                TEAM_WINNER_ID=$($PSQL "SELECT team_id FROM teams WHERE name='$WINNER'")
                if [[ $INSERT_WINNER_RESULT ==  "INSERT 0 1" ]]
                then
                    echo Inserted and team, $WINNER,
                fi
            fi
            # get team OPPONENT id
            TEAM_OPPONENT_ID=$($PSQL "SELECT team_id FROM teams WHERE name='$OPPONENT'")
            # if OPPONENT_id not found
            if [[ -z $TEAM_OPPONENT_ID ]]
            then
                # insert team OPPONENT
                INSERT_OPPONENT_RESULT=$($PSQL "INSERT INTO teams(name) VALUES('$OPPONENT')")
                TEAM_OPPONENT_ID=$($PSQL "SELECT team_id FROM teams WHERE name='$OPPONENT'")
                if [[ $INSERT_OPPONENT_RESULT ==  "INSERT 0 1" ]]
                then
                    echo Inserted and team, $OPPONENT
                fi
            fi
            # insert year
            INSERT_YEAR_RESULT=$($PSQL "INSERT INTO games(year, round,winner_id , opponent_id, winner_goals, opponent_goals)VALUES('$YEAR', '$ROUND', '$TEAM_WINNER_ID', '$TEAM_OPPONENT_ID', '$WINNER_GOALS', '$OPPONENT_GOALS')")
            if [[ $INSERT_YEAR_RESULT == "INSERT 0 1" ]]
            then
                echo Inserted into games and teams, "$YEAR |$ROUND | $TEAM_WINNER_ID | $TEAM_OPPONENT_ID | $WINNER_GOALS| $OPPONENT_GOALS"
            fi
            # get new game_id
            GAME_ID=$($PSQL "SELECT game_id FROM games WHERE year='$YEAR' AND round='$ROUND' AND winner_id IS NOT NULL AND opponent_id IS NOT NULL and winner_goals='$WINNER_GOALS' AND opponent_goals='$OPPONENT_GOALS'")
        fi
  fi
done
