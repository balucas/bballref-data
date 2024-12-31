import React from 'react';

const Dashboard: React.FC = () => {
    return (
        <div className="p-5 bg-gray-100">
            <p>header here</p>
            <p>search bar here</p>
            <div className="grid gap-5 lg:grid-cols-3">
                <div className="lg:col-span-1">
                    <p>player info here</p>
                </div>
                <div className="lg:col-span-2">
                    <p>player stats here</p>
                </div>
            </div>
        </div>
    );
};
export default Dashboard;