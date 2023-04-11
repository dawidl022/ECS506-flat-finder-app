import { FC, useState } from "react";
import { useRouter } from "next/router";

import React from "react";
import useApi from "@/hooks/useApi";

import { User } from "@/generated";
import useUser from "@/hooks/useUser";

import styles from "./Admin.module.scss";

const AdminPanel: FC = () => {
  const { apiManager } = useApi();
  const { user: currentUser } = useUser();
  // const currentUserId = user?.id;
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);
  const [isCurrentUserAdmin, setIsAdmin] = useState<boolean>(false);
  const router = useRouter();

  React.useEffect(() => {
    // get users
    apiManager
      .apiV1UsersGet()
      .then((users: User[]) => {
        setUsers(users);
      })
      .catch(() => setError(true));
  }, []);

  const removeUserFromSystem = (user: User) => {
    if (confirm("Are you sure you want to remove " + user.email + "?")) {
      apiManager
        .apiV1UsersUserIdDelete({ userId: user.id })
        .then(() => {
          setUsers(users.filter(u => u.id !== user.id));
        })
        .catch(err => {
          alert("User failed to be removed. \nError:" + err);
        });
    }
  };

  const grantAdmin = (user: User) => {
    if (confirm("Are you sure you want to grant " + user.email + " admin?")) {
      apiManager
        .apiV1AdminsUserIdPut({ userId: user.id })
        .then(() => {
          router.reload();
        })
        .catch(err => {
          alert("User failed to be granted administrator role. \nError:" + err);
        });
    }
  };

  const revokeAdmin = (user: User) => {
    if (
      confirm(
        "Are you sure you want to revoke " + user.email + "'s admin role?"
      )
    ) {
      apiManager
        .apiV1AdminsUserIdDelete({ userId: user.id })
        .then(() => {
          router.reload();
        })
        .catch(err => {
          alert(
            "User's administrator role failed to be revoked . \nError:" + err
          );
        });
    }
  };

  React.useEffect(() => {
    if (currentUser?.id) {
      apiManager
        .apiV1AdminsUserIdGet({ userId: currentUser.id })
        .then(() => {
          setIsAdmin(true);
        })
        .catch(err => {
          console.log(err);
        })
        .finally(() => {
          setIsLoading(false);
        });
    }
  }, [currentUser]);

  if (isLoading) {
    return <p>Loading</p>;
  } else if (!isCurrentUserAdmin) {
    return (
      <div>
        <p> Administrator Access Only </p>
        <button type="button" onClick={() => router.push("/")}>
          Return To Homepage
        </button>
      </div>
    );
  } else if (error) {
    return <p>Error fetching data</p>;
  } else {
    return (
      <div className={styles.wrapper}>
        {/* get each user and display their email */}
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Admin </th>
              <th>Remove User</th>
              <th>Admin Command</th>
            </tr>
          </thead>
          <tbody>
            {!users ? (
              <tr>
                <td>Loading</td>
              </tr>
            ) : (
              users.map((user: User, index) => {
                return (
                  <tr key={index}>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.isAdmin ? "Yes" : "No"}</td>
                    {user.id === currentUser?.id ? (
                      <td></td>
                    ) : (
                      <td className={styles.adminRevoke}>
                        <button
                          type="button"
                          onClick={() => removeUserFromSystem(user)}
                        >
                          Remove User
                        </button>
                      </td>
                    )}
                    {user.isAdmin ? (
                      <>
                        {user.id === currentUser?.id ? (
                          <td></td>
                        ) : (
                          <td className={styles.adminRevoke}>
                            <button
                              type="button"
                              onClick={() => {
                                revokeAdmin(user);
                              }}
                            >
                              Revoke Admin
                            </button>
                          </td>
                        )}
                      </>
                    ) : (
                      <td className={styles.adminGrant}>
                        <button
                          type="button"
                          onClick={() => {
                            grantAdmin(user);
                          }}
                        >
                          Grant Admin
                        </button>
                      </td>
                    )}
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    );
  }
};

export default AdminPanel;
