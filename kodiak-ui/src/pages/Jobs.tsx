import React from "react";
import JobTable from "../components/JobTable";
import {jobsList} from "../stubs/jobs";

const Jobs = () => {
    return (
        <>
            <JobTable jobs={jobsList}/>
        </>
    )
}

export default Jobs;