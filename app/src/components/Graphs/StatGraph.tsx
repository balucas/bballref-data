import React from 'react';
import { ResponsiveLine } from '@nivo/line';
import { Gamelog, getField } from '../../types/Gamelog';

type StatGraphProps = {
    data: Gamelog[]; // Array of gamelogs
    color: string; // Line color
    statName: string; // Name of the stat to graph
    title?: string; // Title of the graph
};

const StatGraph: React.FC<StatGraphProps> = ({ data, color, statName, title }) => {
    // Transform the data into Nivo's expected format
    console.log("here is statname: " + statName + ", and here is data: " + data[0][statName]);
    const nivoData = [
        {
            id: statName,
            color,
            data: data.map((d) => ({
                x: new Date(d.date_game).toLocaleDateString(), // Convert ISO8601 to date string
                y: d[statName] as number | string | null,
            })), // Map games to x, values to y
        },
    ];

    return (
        <div style={{ height: 400 }}>
            <ResponsiveLine
                data={nivoData}
                margin={{ top: 50, right: 50, bottom: 50, left: 60 }}
                xScale={{ type: 'point' }} // Ensures equidistant points
                yScale={{
                    type: 'linear',
                    min: 'auto', // Automatically adjusts based on data
                    max: 'auto',
                    stacked: false,
                    reverse: false,
                }}
                axisBottom={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'Game',
                    legendPosition: 'middle',
                    legendOffset: 36,
                }}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: '',
                    legendPosition: 'middle',
                    legendOffset: -50,
                }}
                colors={{ datum: 'color' }} // Use the color provided by the parent
                pointSize={10}
                pointColor={{ from: 'color', modifiers: [] }}
                pointBorderWidth={2}
                pointBorderColor={{ from: 'serieColor' }}
                enablePointLabel={true}
                pointLabel={(d) => `${d.data.y}`} // Show value on the points
                pointLabelYOffset={-12}
                useMesh={true} // Improves tooltip and interactivity
                tooltip={({ point }) => (
                    <div
                        style={{
                            background: 'white',
                            padding: '5px',
                            border: `1px solid ${point.borderColor}`,
                            borderRadius: '4px',
                        }}
                    >
                        <strong>Game {point.data.xFormatted}</strong>: {point.data.yFormatted} {statName}
                    </div>
                )}
            />
        </div>
    );
};

export default StatGraph;