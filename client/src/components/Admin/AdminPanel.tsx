import { FC, useState } from "react";
import { useRouter } from "next/router";
import { Configuration, DefaultApi } from "@/generated";

import { User } from "@/generated";

interface AdminPanelProps {
  currentUserId: string;
}
const AdminPanel: FC<AdminPanelProps> = ({ currentUserId }) => {
  const api = new DefaultApi(
    new Configuration({ basePath: "http://127.0.0.1:5000" })
  );
  const [users, setUsers] = useState<User[]>([]);
  let isCurrentUserAdmin = false;
  const router = useRouter();

  api
    .apiV1UsersGet()
    .then((users: User[]) => {
      setUsers(users);
    })
    .catch(err => {
      alert(err);
    });

  const removeUserFromSystem = (user: User) => {
    if (confirm("Are you sure you want to remove " + user.email + "?")) {
      api
        .apiV1UsersUserIdDelete({ userId: user.id })
        .then(() => {
          setUsers(users.filter((user: User) => user.id !== user.id));
        })
        .catch(err => {
          alert("User failed to be removed. \nError:" + err);
        });
    }
  };

  const grantAdmin = (user: User) => {
    if (confirm("Are you sure you want to grant " + user.email + " admin?")) {
      api
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
      api
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

  api.apiV1AdminsUserIdGet({ userId: currentUserId }).then(res => {
    isCurrentUserAdmin = true;
  });

  if (!isCurrentUserAdmin) {
    return (
      <div>
        <h3> Administrator Access Only </h3>
        <button type="button" onClick={() => router.push("/index")}>
          Return To Homepage
        </button>
      </div>
    );
  } else {
    return (
      <div>
        {/* get each user and display their email */}
        <table>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Admin </th>
          </tr>

          {users.map((user: User, index) => {
            return (
              <tr key={index}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.isAdmin ? "Yes" : "No"}</td>
                {user.id === currentUserId ? (
                  <td></td>
                ) : (
                  <td>
                    <button
                      type="button"
                      onClick={() => removeUserFromSystem(user)}
                    >
                      Remove User
                    </button>
                  </td>
                )}

                {user.isAdmin ? (
                  <td>
                    <button
                      type="button"
                      onClick={() => {
                        revokeAdmin(user);
                      }}
                    >
                      Revoke Admin
                    </button>
                  </td>
                ) : (
                  <td>
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
          })}
        </table>
      </div>
    );
  }
};

export default AdminPanel;
