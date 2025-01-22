import React from 'react';
import '../css/LogInSignUp.css';
import { InputAdornment } from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import { InputBase } from "@mui/material";
import PersonIcon from '@mui/icons-material/Person';

function LogInSignUp() {


    return (
        <div className="main">

            <div className="signup">
                <h1 className='title'>log in</h1>
                <div className='decoration-bar'></div>
                <form>
                    <div className="input-container">
                        <InputBase
                            placeholder="Account ID"
                            type="password"
                            startAdornment={
                                <InputAdornment position="start">
                                    <PersonIcon />
                                </InputAdornment>
                            }

                        />;
                    </div>
                    <div className="input-container">
                        <InputBase
                            placeholder="Password"
                            type="password"
                            startAdornment={
                                <InputAdornment position="start">
                                    <LockIcon />
                                </InputAdornment>
                            }

                        />;
                    </div>
                </form>

                <div className="signup-button">
                    <h4> Don't have an account or forgot your password? Click here </h4>
                </div>
            </div>



        </div>
    );
}

export default LogInSignUp;
