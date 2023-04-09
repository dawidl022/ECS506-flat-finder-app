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
  const [error, setError] = useState(false);
  const [isCurrentUserAdmin, setIsAdmin] = useState<boolean>(false);
  const router = useRouter();

  api
    .apiV1UsersGet()
    .then((users: User[]) => {
      setUsers(users);
    })
    .catch(() => setError(true));


  const removeUserFromSystem = (user : User) => {
    if (confirm("Are you sure you want to remove " + users[index].email + "?")) {
      api.apiV1UsersUserIdDelete({ userId: user.id }).then(() => {
        setUsers(users.filter((u) => u.id !== user.id));
      }).catch(err => {
        alert("User failed to be removed. \nError:" + err);
      });
    }
  };

  api.apiV1AdminsUserIdGet({ userId: currentUserId }).then(() => {
    setIsAdmin(true);
  });

  if (!isCurrentUserAdmin) {
    return (
      <div>
        {error ? (
        <p>Error fetching data</p>
      ) : !users ? (
        <p>Loading</p>
      ) : (
        <><p> Administrator Access Only </p><button type="button" onClick={() => router.push("/index")}>
                Return To Homepage
              </button></>    
      )}
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
              </tr>
            );
          })}
        </table>
      </div>
    );
  }
};

export default AdminPanel;
