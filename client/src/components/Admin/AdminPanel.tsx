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
    if (confirm("Are you sure you want to remove " + users[index].name + "?")) {
      const updatedUsers = [...users];
      updatedUsers.splice(index, 1);
      setUsers(updatedUsers);
      api
        .apiV1UsersUserIdDelete({ userId: users[index].id })
        .then(res => {
          console.log(res);
        })
        .catch(err => {
          alert("User failed to be removed. \nError:" + err);
        });
    }
  };

  users.map((user: User) => {
    if (user.id === currentUserId && !user.isAdmin) {
      isCurrentUserAdmin = true;
    } else {
      return;
    }
  });

  if (isCurrentUserAdmin) {
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
        {users.map((user: User, index) => {
          {
            if (user.id === currentUserId) {
              return (
                <div key={index}>
                  <table>
                    <tr>
                      <td>{user.name}</td>
                      <td>Email: {user.email}</td>
                      <td>Admin permissions: {user.isAdmin.toString()} </td>
                    </tr>
                  </table>
                </div>
              );
            } else {
              return (
                <div key={index}>
                  <table>
                    <tr>
                      <td>{user.name}</td>
                      <td>Email: {user.email}</td>
                      <td>Admin permissions: {user.isAdmin.toString()} </td>
                      <button
                        type="button"
                        onClick={() => removeUserFromSystem(index)}
                      >
                        Remove User
                      </button>
                    </tr>
                  </table>
                </div>
              );
            }
          }
        })}
      </div>
    );
  }
};

export default AdminPanel;
