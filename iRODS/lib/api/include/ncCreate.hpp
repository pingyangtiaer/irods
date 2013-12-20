/*** Copyright (c), The Regents of the University of California            ***
 *** For more information please refer to files in the COPYRIGHT directory ***/
/* ncCreate.h
 */

#ifndef NC_CREATE_HPP
#define NC_CREATE_HPP

/* This is a NETCDF API call */

#include "rods.hpp"
#include "rcMisc.hpp"
#include "procApiRequest.hpp"
#include "apiNumber.hpp"
#include "initServer.hpp"
#include "dataObjInpOut.hpp"
#include "ncOpen.hpp"

#if defined(RODS_SERVER) && defined(NETCDF_API)
#define RS_NC_CREATE rsNcCreate
/* prototype for the server handler */
int
rsNcCreate( rsComm_t *rsComm, ncOpenInp_t *ncCreateInp, int **ncid );
#else
#define RS_NC_CREATE NULL
#endif

extern "C" {

    /* prototype for the client call */
    /* rcNcCreate - netcdf create an iRODS data object (equivalent to nc_open.
     * Input -
     *   rcComm_t *conn - The client connection handle.
     *   ncOpenInp_t *ncCreateInp - generic nc open/create input. Relevant items are:
     *	objPath - the path of the data object.
     *      mode - the mode of the create - valid values are given in netcdf.h -
     *       NC_NOCLOBBER, NC_SHARE, NC_64BIT_OFFSET, NC_NETCDF4, NC_CLASSIC_MODEL.
     *	condInput - condition input (not used).
     * OutPut -
     *   int the ncid of the opened object - an integer descriptor.
     */

    int
    rcNcCreate( rcComm_t *conn, ncOpenInp_t *ncCreateInp, int *ncid );

    int
    _rcNcCreate( rcComm_t *conn, ncOpenInp_t *ncCreateInp, int **ncid );

}

#endif	/* NC_CREATE_H */
