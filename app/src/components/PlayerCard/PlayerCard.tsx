import React from 'react';
import StatGraph from '../Graphs/StatGraph';
import { Gamelog } from '../../types/Gamelog';

interface PlayerCardProps {
    playerName: string;
    gamelogs: Gamelog[];
    statNames: string[];
}

const PlayerCard: React.FC<PlayerCardProps> = ({ playerName, gamelogs, statNames }) => {

    // Creates "smaller" gamelogs for each stat 
    // Rationale is to allow each graph flexibility in what additional game information to display
    // rather than restricting to a single stat
    const stats: { statName: string,  logs: Gamelog[] }[] = []
    statNames.forEach((statName) => {
        stats.push({ statName, logs: [] });
    });

    gamelogs.forEach((gamelog) => {
        stats.forEach((stat) => {
            const statGamelog: Gamelog = {
                _id: gamelog._id,
                date_game: gamelog.date_game,
                season: gamelog.season,
                status: gamelog.status,
                opp_id: gamelog.opp_id
            }
            
            statGamelog[stat.statName] = gamelog[stat.statName];
            stat.logs.push(statGamelog)
        });
    });

    return (
        <div className="player-card">
            <h2>{playerName}</h2>
            <div className="player-stats">
                {stats.map((statData) => (
                    <StatGraph 
                        color="blue"
                        key={statData.statName} 
                        statName={statData.statName} 
                        data={statData.logs} />
                ))}
            </div>
        </div>
    );
};

export default PlayerCard;