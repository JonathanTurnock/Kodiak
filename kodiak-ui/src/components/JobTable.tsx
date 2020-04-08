import React from 'react';
import {Job} from "../types/job";

const JobTable: React.FC<{ jobs: Job[] }> = ({jobs}) => {
    return (<div style={{paddingTop: 32}} className={"container"}>
        <table className="table table-hover">
            <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">Repo</th>
                <th scope="col"/>
            </tr>
            </thead>
            <tbody>
            {jobs.map((job) => <JobRow job={job}/>)}
            </tbody>
        </table>
    </div>)
}

const JobRow: React.FC<{ job: Job }> = ({job}) => {
    return (<tr>
        <th scope="row">{job.id}</th>
        <td>{job.name}</td>
        <td>{job.repo}</td>
        <td>
            <button className={"btn btn-success"}>Run</button>
        </td>
    </tr>)
}

export default JobTable;