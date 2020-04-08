import React from 'react';
import RunTable from "../components/RunTable";
import {runsList} from "../stubs/runs";

const Runs = () => {
    return (
        <>
            <RunTable runs={runsList}/>
        </>
    )
}

export default Runs