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

  const removeUserFromSystem = (index: number) => {
    if (
      confirm("Are you sure you want to remove " + users[index].email + "?")
    ) {
      api
        .apiV1UsersUserIdDelete({ userId: users[index].id })
        .then(() => {
          setUsers(users.filter((user: User) => user.id !== users[index].id));
        })
        .catch(err => {
          alert("User failed to be removed. \nError:" + err);
        });
    }
  };

  const grantAdmin = (index: number) => {
    if (
      confirm(
        "Are you sure you want to grant " + users[index].email + " admin?"
      )
    ) {
      api
        .apiV1AdminsUserIdPut({ userId: users[index].id })
        .then(() => {
          setUsers(users.filter((user: User) => user.id !== users[index].id));
        })
        .catch(err => {
          alert("User failed to be granted administrator role. \nError:" + err);
        });
    }
  };

  const revokeAdmin = (index: number) => {
    if (
      confirm(
        "Are you sure you want to revoke " +
          users[index].email +
          "'s admin role?"
      )
    ) {
      api
        .apiV1AdminsUserIdDelete({ userId: users[index].id })
        .then(() => {
          setUsers(users.filter((user: User) => user.id !== users[index].id));
        })
        .catch(err => {
          alert("User's administrator role failed to be revoked . \nError:" + err);
        })
    }
  };

  api.apiV1AdminsUserIdGet({ userId: currentUserId }).then(() => {});

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
                      onClick={() => removeUserFromSystem(index)}
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
                        revokeAdmin(index);
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
                        grantAdmin(index);
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
