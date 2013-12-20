/*** Copyright (c), The Regents of the University of California            ***
 *** For more information please refer to files in the COPYRIGHT directory ***/
/* userAdmin.h
 */

/* This client/server call is used for user-level (non-admin)
   administrative functions.  It is non-privileged for use by regular
   users for certain updates, such as changing their password. */

#ifndef USER_ADMIN_HPP
#define USER_ADMIN_HPP

/* This is a Metadata type API call */

#include "rods.hpp"
#include "rcMisc.hpp"
#include "procApiRequest.hpp"
#include "apiNumber.hpp"
#include "initServer.hpp"
#include "icatDefines.hpp"

typedef struct {
    char *arg0;
    char *arg1;
    char *arg2;
    char *arg3;
    char *arg4;
    char *arg5;
    char *arg6;
    char *arg7;
    char *arg8;
    char *arg9;
} userAdminInp_t;

#define userAdminInp_PI "str *arg0; str *arg1; str *arg2; str *arg3; str *arg4; str *arg5; str *arg6; str *arg7;  str *arg8;  str *arg9;"

extern "C" {

#if defined(RODS_SERVER)
#define RS_USER_ADMIN rsUserAdmin
    /* prototype for the server handler */
    int
    rsUserAdmin( rsComm_t *rsComm, userAdminInp_t *userAdminInp );

    int
    _rsUserAdmin( rsComm_t *rsComm, userAdminInp_t *userAdminInp );
#else
#define RS_USER_ADMIN NULL
#endif

    /* prototype for the client call */
    int
    rcUserAdmin( rcComm_t *conn, userAdminInp_t *userAdminInp );

}

#endif	/* USER_ADMIN_H */
