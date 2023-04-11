# Acceptance tests

<table>
  <thead>
    <tr>
      <th>Use case</th>
      <th>Steps and Required Inputs</th>
      <th>Expected behaviour</th>
      <th>Observed behaviour</th>
    <tr>
  </thead>
  <tbody>
    <tr>
      <td>Login</td>
      <td>
        <ol>
          <li>Add user email to list of test users in Google Cloud Console</li>
          <li>Navigate to home page</li>
          <li>Click login with Google</li>
          <li>Enter login details associated with account added in step 1</li>
          <li>Accept Google OAuth conditions</li>
        </ol>
      </td>
      <td>
        User redirected back to application, logged in and prompted to complete
        their profile
      </td>
      <td></td>
    </tr>
    <tr>
      <td>Login</td>
      <td>
        <ol>
          <li>Navigate to home page</li>
          <li>Click login with Google</li>
          <li>Enter login details associated with account never added</li>
        </ol>
      </td>
      <td>
        User not granted access to the application
      </td>
      <td></td>
    </tr>
    <tr>
      <td>Complete Profile</td>
      <td>
        <ol>
          <li>Login as a new user</li>
          <li>Enter "Dawid" into first name input field, "Lachowicz" into last name.</li>
          <li>Leave phone number blank</li>
          <li>Press "Save details" button</li>
        </ol>
      </td>
      <td>
        Complete profile popup disappears and "Dawid L." is visible in the navbar
      </td>
      <td></td>
    </tr>
    <tr>
      <td>Complete Profile</td>
      <td>
        <ol>
          <li>Login as a new user</li>
          <li>Leave all fields blank</li>
          <li>Press "Save details" button</li>
        </ol>
      </td>
      <td>
        Prompt telling the user to fill in "First name" and "Last name" fields
      </td>
      <td></td>
    </tr>
    <tr>
      <td>View accommodation listings</td>
      <td>
        <ol>
          <li>Login</li>
          <li>Enter "London" in location and "10" in radius fields in the search box</li>
          <li>Press "Search" button</li>
        </ol>
      </td>
      <td>
        List of accommodation listings pulled from
        <a href="https://www.zoopla.co.uk/">Zoopla</a> appears
      </td>
      <td></td>
    </tr>
    <tr>
      <td>View accommodation listings</td>
      <td>
        <ol>
          <li>Login</li>
          <li>Leave all fields blank in the search box</li>
          <li>Press "Search" button</li>
        </ol>
      </td>
      <td>
        Prompt telling the user to fill in "Location" and "radius" fields
      </td>
      <td></td>
    </tr>
    <tr>
      <td>Create accommodation accommodation</td>
      <td>
        <ol>
          <li>Login</li>
          <li>Open navbar and click "Create Listing"</li>
          <li>Select accommodation tab</li>
          <li>Fill in all fields with some dummy data (e.g. a room for rent at QMUL)</li>
          <li>Upload at least 1 photo</li>
          <li>Click "Submit button"</li>
        </ol>
      </td>
      <td>
        User redirected to the profile page containing the newly created
        listing. Upon searched for accommodation listings within radius of the
        created listing, the listing appears in the search results
      </td>
      <td></td>
    </tr>
    <tr>
      <td>Create accommodation accommodation</td>
      <td>
        <ol>
          <li>Login</li>
          <li>Open navbar and click "Create Listing"</li>
          <li>Select accommodation tab</li>
          <li>Leave all fields blank</li>
          <li>Click "Submit button"</li>
        </ol>
      </td>
      <td>
        Prompt telling the user to fill in missing fields
      </td>
      <td></td>
    </tr>
  </tbody>
</table>
