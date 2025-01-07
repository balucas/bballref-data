import React from 'react';
import StatGraph from '../../components/Graphs/StatGraph';
import PlayerCard from '../../components/PlayerCard/PlayerCard';
import { Gamelog } from '../../types/Gamelog';
import { mockGamelogData } from '../../utils/mockData';

const Dashboard: React.FC = () => {
    const statData = mockGamelogData.data as Gamelog[];
    return (
        <div className="w-full h-full p-5 bg-gray-100">
            <p>header here</p>
            <p>search bar here</p>
            <div className="grid gap-5 lg:grid-cols-6">
            <div className="lg:col-span-1">
                <p>player info here</p>
            </div>
            <div className="lg:col-span-5">
                <StatGraph color='blue' data={statData} statName="pts" />
            </div>
            </div>
        </div>
    );
};
export default Dashboard;