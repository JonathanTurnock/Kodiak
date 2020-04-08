import React from 'react';
import {Run} from "../types/run";
import {formatDistance, formatDistanceToNow} from "date-fns";

const RunTable: React.FC<{ runs: Run[] }> = ({runs}) => {
    return (<div style={{paddingTop: 32}} className={"container"}>
        <table className="table table-hover">
            <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Job ID</th>
                <th scope="col">Status</th>
                <th scope="col">Started</th>
                <th scope="col">Duration</th>
                <th scope="col"/>
            </tr>
            </thead>
            <tbody>
            {runs.map((run) => <RunRow run={run}/>)}
            </tbody>
        </table>
    </div>)
}

const RunRow: React.FC<{ run: Run }> = ({run}) => {
    return (<tr>
        <th scope="row">{run.id}</th>
        <td>{run.job_id}</td>
        <td>{run.status}</td>
        <td>{`${formatDistanceToNow(run.started)} ago`}</td>
        <td>{formatDistance(run.started, run.ended, {includeSeconds: true})}</td>
        <td>
            <button className={"btn btn-success"}>Action</button>
        </td>
    </tr>)
}

export default RunTable;